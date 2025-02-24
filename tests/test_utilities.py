import logging
from unittest.mock import patch

import pytest
import requests

from cloud_run_ingestion.ingestion.models import Fixture
from cloud_run_ingestion.ingestion.utilities import (
    call_api,
    extract_and_validate_entities,
)


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


def test_extract_and_validate_entities_succeeds(caplog, valid_fixtures_raw_data):
    with caplog.at_level(logging.WARNING):
        validated_entities = extract_and_validate_entities(
            valid_fixtures_raw_data, Fixture
        )
    assert len(validated_entities) == 2
    assert (
        f"Validation completed with 1 errors for {Fixture.__name__.lower()}"
        not in caplog.text
    )


def test_extract_and_validate_entities_raises_validation_error(
    caplog, invalid_fixtures_raw_data
):
    with caplog.at_level(logging.WARNING):
        validated_entities = extract_and_validate_entities(
            invalid_fixtures_raw_data, Fixture
        )
    assert len(validated_entities) == 0
    assert (
        f"Validation completed with {len(invalid_fixtures_raw_data)} errors for {Fixture.__name__.lower()}"
        in caplog.text
    )


def test_extract_and_validate_entities_empty_list(caplog):
    entities = []
    with caplog.at_level(logging.WARNING):
        validated_entities = extract_and_validate_entities(entities, Fixture)
    assert validated_entities == []
    assert f"No data found for {Fixture.__name__.lower()}" in caplog.text
