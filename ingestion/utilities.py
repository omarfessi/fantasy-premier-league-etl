import logging

import requests
from models import Event, Fixture, Player, Team
from pydantic import ValidationError


def call_api(bootstrap_static_url: str) -> requests.models.Response:
    payload = {}
    headers = {}
    response = requests.request(
        "GET", bootstrap_static_url, headers=headers, data=payload
    )
    return response


ModelUnion = Event | Team | Player | Fixture


def extract_and_validate_entities(
    entities: list[dict], model_type: ModelUnion
) -> list[ModelUnion]:
    """
    Extract and validate entities using a specified Pydantic model.

    Args:
        entities (List[dict]): List of entity dictionaries to validate.
        model_type (ModelUnion): Pydantic model class for validation.

    Returns:
        List[ModelUnion]: Validated data and log a List of error messages.
    """
    data = []
    errors = []
    for entity in entities:
        try:
            data.append(model_type(**entity))
        except ValidationError as e:
            errors.append(
                f"Error validating {model_type.__name__.lower()}: {entity} with error: {e}"
            )
    if errors:
        error_message = "\n".join(errors)
        logging.error(error_message)
    return data
