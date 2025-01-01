import logging
from unittest.mock import patch

import pytest
import requests
from pydantic import BaseModel

from ingestion.utilities import call_api, extract_and_validate_entities


def test_call_api_success():
    url = "http://example.com"

    with patch("requests.request", return_value=requests.Response()) as mock_request:
        mock_request.return_value.status_code = 200
        response = call_api(url)
        assert response.status_code == 200


def test_call_api_failure():
    url = "http://example.com"

    with patch("requests.request", return_value=requests.Response()) as mock_request:
        mock_request.return_value.status_code = 500
        with pytest.raises(requests.exceptions.RequestException) as exc_info:
            call_api(url)

        # Verify SystemExit was raised with exit code 1
        assert exc_info.type is requests.exceptions.RequestException
        assert (
            exc_info.value.args[0]
            == f"Failed to fetch data from {url} with status code: {mock_request.return_value.status_code}, \
                   ingestion pipeline failed."
        )


class MockModel(BaseModel):
    id: int
    name: str


def test_extract_and_validate_entities_success():
    entities = [{"id": 1, "name": "Entity1"}, {"id": 2, "name": "Entity2"}]
    validated_entities = extract_and_validate_entities(entities, MockModel)
    assert len(validated_entities) == 2
    assert validated_entities[0].id == 1
    assert validated_entities[0].name == "Entity1"
    assert validated_entities[1].id == 2
    assert validated_entities[1].name == "Entity2"


def test_extract_and_validate_entities_validation_error(caplog):
    entities = [{"id": 1, "name": "Entity1"}, {"id": "invalid_id", "name": "Entity2"}]
    with caplog.at_level(logging.WARNING):
        validated_entities = extract_and_validate_entities(entities, MockModel)
    assert len(validated_entities) == 1
    assert validated_entities[0].id == 1
    assert validated_entities[0].name == "Entity1"
    assert "Validation completed with 1 errors for mockmodel" in caplog.text
    print(caplog.text)


def test_extract_and_validate_entities_empty_list(caplog):
    entities = []
    with caplog.at_level(logging.WARNING):
        validated_entities = extract_and_validate_entities(entities, MockModel)
    assert validated_entities == []
    assert "No data found for mockmodel" in caplog.text
