import logging

import requests
from models import ModelUnion
from pydantic import ValidationError


def call_api(bootstrap_static_url: str) -> requests.models.Response:
    """
    Makes a GET request to the specified URL and returns the response.

    Args:
        url (str): The URL to which the GET request is made.

    Returns:
        requests.models.Response: The response object from the GET request.
    """
    payload = {}
    headers = {}
    response = requests.request(
        "GET", bootstrap_static_url, headers=headers, data=payload
    )
    if response.status_code != 200:
        logging.error(
            f"Failed to fetch data from {bootstrap_static_url} with status code: {response.status_code}"
        )
    return response


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
    if not entities:
        logging.error(f"No data found for {model_type.__name__.lower()}")
    for entity in entities:
        try:
            data.append(model_type(**entity))
        except ValidationError as e:
            errors.append(
                f"Failed to validate {model_type.__name__.lower()}: {entity} with error: {e}"
            )
    if errors:
        error_message = "\n".join(errors)
        logging.warning(error_message)
    return data
