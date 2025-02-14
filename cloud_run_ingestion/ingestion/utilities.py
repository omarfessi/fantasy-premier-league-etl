import logging
import os
import tempfile

import duckdb
import google.cloud.storage
import pyarrow as pa
import pyarrow.parquet as pq
import requests
from pydantic import ValidationError

from .models import ModelUnion


def call_api(bootstrap_static_url: str) -> requests.models.Response:
    """
    Makes a GET request to the specified URL and returns the response.

    Args:
        url (str): The URL to which the GET request is made.

    Returns:
        requests.models.Response: The response object from the GET request.
    """
    response = requests.request("GET", bootstrap_static_url)
    if response.status_code != 200:
        raise requests.exceptions.RequestException(
            f"Failed to fetch data from {bootstrap_static_url} with status code: {response.status_code}, \
                ingestion pipeline failed."
        )
    return response


def extract_and_validate_entities(entities: list[dict], model_type: ModelUnion) -> list[ModelUnion]:
    """
    Extract and validate entities using a specified Pydantic model.

    Args:
        entities (List[dict]): List of entity dictionaries to validate.
        model_type (ModelUnion): Pydantic model class for validation.

    Returns:
        List[ModelUnion]: Validated data and log a List of error messages.
    """
    data = []
    if not entities:
        logging.warning(f"No data found for {model_type.__name__.lower()}")
        return data
    errors = []
    for entity in entities:
        try:
            data.append(model_type(**entity))
        except ValidationError as e:
            errors.append(f"Failed to validate {model_type.__name__.lower()}: {entity} with error: {e}")
    if errors:
        logging.warning(
            f"Validation completed with {len(errors)} errors for {model_type.__name__.lower()}.\n"
            f"Errors:\n{'\n'.join(errors)}"
        )
    return data


def upload_to_gcs(
    client: google.cloud.storage.client.Client,
    bucket_name: str,
    destination_blob_name: str,
    table: pa.Table,
) -> None:
    """
    Upload a PyArrow Table as a Parquet file to a GCS bucket.

    Args:
        bucket_name (str): The name of the GCS bucket.
        destination_blob_name (str): The destination path within the bucket.
        table (pa.Table): The PyArrow Table to upload.
    """
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Create a temporary file for the Parquet data
    with tempfile.NamedTemporaryFile(suffix=".parquet", delete=True) as temp_file:
        # Write PyArrow Table to Parquet file
        pq.write_table(table, temp_file.name)
        logging.info(f"Parquet file created at {temp_file.name}")

        # Upload the file to GCS
        blob.upload_from_filename(temp_file.name)
        logging.info(f"File {destination_blob_name} uploaded to GCS bucket {bucket_name}.")


class TableLoadingBuffer:
    def __init__(
        self,
        database_name: str = "fpl",
        destination="local",
        dryrun: bool = False,
        chunk_size: int = 50000,
    ) -> None:
        self.database_name = database_name
        self.destination = destination
        self.dryrun = dryrun
        self.chunk_size = chunk_size
        # self.conn = self.initialize_connection(destination)

    def initialize_connection(self, destination: str) -> duckdb.DuckDBPyConnection:
        if destination == "md":
            logging.info("Connecting to MotherDuck...")
            if not os.environ.get("MOTHERDUCK_TOKEN"):
                raise ValueError("MotherDuck token is required. Set the environment variable 'MOTHERDUCK_TOKEN'.")
            conn = duckdb.connect("md:")
            conn.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name}")
            conn.execute(f"USE {self.database_name}")
        else:
            conn = duckdb.connect(database=f"{self.database_name}.db")
        return conn

    def insert_table(self, table_name: str, table: pa.Table, duckdb_schema: str) -> None:
        if not self.dryrun:
            logging.info(f"creating table {table_name} in {self.database_name} if not exists")
            self.conn.execute(duckdb_schema)  # Create table in duckdb if not exists using it's schema
            total_inserted = 0
            total_rows = table.num_rows
            for batch_start in range(0, total_rows, self.chunk_size):
                batch_end = min(batch_start + self.chunk_size, total_rows)
                chunk = table.slice(batch_start, batch_end - batch_start)
                self.insert_chunk(chunk, table_name)
                logging.info(f"Inserted chunk {batch_start} to {batch_end}")
            total_inserted += total_rows
            logging.info(f"Total inserted into {table_name}: {total_inserted} rows")

    def insert_chunk(self, chunk: pa.Table, table_name: str) -> None:
        # DuckDB does not recognize the syntax used to query a
        # PyArrow Table directly through
        # INSERT INTO with SELECT * FROM pyarrow.Table.
        # Specifically, the column schema details, including the colon (:) notation,
        # sappear when you're using pyarrow.Table objects directly.
        self.conn.register("buffer_table", chunk)
        insert_query = f"INSERT INTO {table_name} SELECT * FROM buffer_table;"
        logging.info(f"Inserting chunk into {table_name} using query: {insert_query}")
        self.conn.execute(insert_query)
        self.conn.unregister("buffer_table")

    def close_connection(self) -> None:
        """
        Close the DuckDB connection to release resources.
        """
        if self.conn:
            logging.info("Closing DuckDB connection.")
            self.conn.close()
            self.conn = None
            logging.info("DuckDB connection closed.")
