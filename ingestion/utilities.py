import logging

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
    if not entities:
        logging.warning(f"No data found for {model_type.__name__.lower()}")
        return data
    errors = []
    for entity in entities:
        try:
            data.append(model_type(**entity))
        except ValidationError as e:
            errors.append(
                f"Failed to validate {model_type.__name__.lower()}: {entity} with error: {e}"
            )
    if errors:
        logging.warning(
            f"Validation completed with {len(errors)} errors for {model_type.__name__.lower()}.\n"
            f"Errors:\n{'\n'.join(errors)}"
        )
    return data
