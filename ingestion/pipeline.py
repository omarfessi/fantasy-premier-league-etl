import logging
from datetime import date

import pyarrow as pa
from google.cloud import storage

from .config import FIXTURES_URL, STATIC_URL
from .models import Event, Fixture, ModelUnion, Player, Team
from .utilities import call_api, extract_and_validate_entities, upload_to_gcs

logging.basicConfig(level=logging.INFO)


def process_entity(entity_name: str, url: str, model: ModelUnion) -> pa.Table | None:
    """
    Generic function to process entities: fetch, validate, and save to file.

    Args:
        entity_name (str): Name of the entity for logging.
        url (str): API endpoint to fetch data from.
        model (BaseModel): Pydantic model for validation.
        schema_method (callable): Method to generate PyArrow schema.
        filename (str): File name for saving data.
    """
    logging.info(f"Processing {entity_name}...")
    data = call_api(url).json()
    if isinstance(data, dict):
        try:
            data = data[entity_name]
        except KeyError:
            logging.error(f"Key '{entity_name}' is missing from the API response.")
            return
    validated_data = extract_and_validate_entities(data, model)
    if validated_data:
        serialized_data = [data.model_dump() for data in validated_data]
        table = pa.Table.from_pylist(serialized_data, schema=model.pyarrow_schema())
        logging.info(f"Completed processing {entity_name}.")
        return table
    else:
        logging.warning(f"No data processed for {entity_name}.")


if __name__ == "__main__":
    today = date.today().strftime("%Y_%m_%d")
    # today = (date.today() + timedelta(days=1)).strftime("%Y_%m_%d")
    # buffer = TableLoadingBuffer()
    client = storage.Client(project="fantasy-premier-league-447918")
    bucket_name = "fantasy-raw-data"

    for entity in [
        ("fixtures", FIXTURES_URL, Fixture, f"fixtures_{today}.parquet"),
        ("elements", STATIC_URL, Player, f"players_{today}.parquet"),
        ("events", STATIC_URL, Event, f"events_{today}.parquet"),
        ("teams", STATIC_URL, Team, f"teams_{today}.parquet"),
    ]:
        table = process_entity(*entity[0:3])
        if table:
            upload_to_gcs(client, bucket_name, entity[-1], table)
            # logging.info(f"Writing {entity[0]} to file...")
            # pq.write_table(table, entity[-1])
            # logging.info(f"Loading {entity[0]} to database...")
            # buffer.insert_table(entity[0], table, entity[2].duckdb_schema())

            # buffer.upload_to_gcs(
            #     bucket_name="gs://fantasy-raw-data",
            #     destination_blob_name=entity[-1],
            #     table=table,
            # )
    # buffer.close_connection()
