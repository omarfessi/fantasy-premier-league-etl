import logging

import pyarrow as pa
import pyarrow.parquet as pq

from .config import FIXTURES_URL, STATIC_URL
from .models import Event, Fixture, ModelUnion, Player, Team
from .utilities import call_api, extract_and_validate_entities

logging.basicConfig(level=logging.INFO)


def process_entity(
    entity_name: str, url: str, model: ModelUnion, filename: str
) -> None:
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
        pq.write_table(table, filename)
        logging.info(f"Completed processing {entity_name}.")
    else:
        logging.warning(
            f"No data processed neither inserted into destination for {entity_name}."
        )


if __name__ == "__main__":
    for entity in [
        ("fixtures", FIXTURES_URL, Fixture, "fixtures.parquet"),
        ("players", STATIC_URL, Player, "players.parquet"),
        ("events", STATIC_URL, Event, "events.parquet"),
        ("teams", STATIC_URL, Team, "teams.parquet"),
    ]:
        process_entity(*entity)
