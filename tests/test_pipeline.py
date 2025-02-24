from datetime import date
import pyarrow.parquet as pq

from cloud_run_ingestion.ingestion.models import Fixture
from cloud_run_ingestion.ingestion.pipeline import process_entity


class TestProcessEntity:
    def test_process_entity_creates_parquet_with_expected_schema(
        self, mocker, validated_fixtures, tmp_path, valid_fixtures_raw_data
    ):
        # Given
        entity_name = "fixtures"
        url = "http://mock-api.com/fixtures"
        model = Fixture

        # Mock API response
        mock_call_api = mocker.patch("cloud_run_ingestion.ingestion.pipeline.call_api")
        mock_call_api.return_value.json.return_value = valid_fixtures_raw_data  # Mocked raw data as it is not important here as it has been already tested

        # Mock extract_and_validate_entities, it has been already tested
        mock_extract_and_validate = mocker.patch(
            "cloud_run_ingestion.ingestion.pipeline.extract_and_validate_entities"
        )
        mock_extract_and_validate.return_value = validated_fixtures

        # When
        table = process_entity(entity_name, url, model)
        # Then
        assert table.num_rows == len(validated_fixtures)
        assert table.schema == model.pyarrow_schema()

    def test_process_entity_logs_error_when_key_is_missing(
        self, mocker, caplog, tmp_path
    ):
        # Given
        today = date.today().strftime("%Y_%m_%d")
        entity_name = "fixtures"
        url = "http://mock-api.com/fixtures"
        model = Fixture

        # Mock API response
        mock_call_api = mocker.patch("cloud_run_ingestion.ingestion.pipeline.call_api")
        mock_call_api.return_value.json.return_value = {
            "wrong_key": [
                {"id": 1, "name": "Fixture 1"}
            ]  # Mocked raw data, not important here as it has been already tested
        }

        # When
        process_entity(entity_name, url, model)

        # Then
        assert "Key 'fixtures' is missing from the API response." in caplog.text

    def test_process_entity_logs_warning_when_no_data_processed(
        self, mocker, caplog, tmp_path
    ):
        # Given
        today = date.today().strftime("%Y_%m_%d")
        entity_name = "fixtures"
        url = "http://mock-api.com/fixtures"
        model = Fixture
        # Mock API response
        mock_call_api = mocker.patch("cloud_run_ingestion.ingestion.pipeline.call_api")
        mock_call_api.return_value.json.return_value = {
            "fixtures": [{"id": 1, "name": "Fixture 1"}]
            # Mocked raw data, not important here as it has been already tested,
            # but fixtures key must be present to avoid KeyError
        }
        mock_extract_and_validate = mocker.patch(
            "cloud_run_ingestion.ingestion.pipeline.extract_and_validate_entities"
        )
        mock_extract_and_validate.return_value = []  # No data

        # When
        process_entity(entity_name, url, model)
        # Then
        assert f"No data processed for {entity_name}." in caplog.text
