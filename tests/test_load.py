import unittest
import os
import pandas as pd
from unittest.mock import patch, Mock, MagicMock
from utils.load import (
    save_to_csv,
    save_to_google_sheets,
    save_to_postgres,
    get_google_sheets_service,
    get_postgres_engine,
)


def sample_df():
    return pd.DataFrame([{
        "Title": "T-shirt 2",
        "Price": 1634400.0,
        "Rating": 3.9,
        "Colors": 3,
        "Size": "M",
        "Gender": "Women",
        "Timestamp": "2025-01-01T00:00:00",
    }])


class TestSaveToCSV(unittest.TestCase):

    def test_save_creates_file(self):
        filepath = "test_products.csv"
        result = save_to_csv(sample_df(), filepath)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(filepath))
        os.remove(filepath)

    def test_empty_df_returns_false(self):
        result = save_to_csv(pd.DataFrame(), "/tmp/empty.csv")
        self.assertFalse(result)

    def test_none_returns_false(self):
        result = save_to_csv(None, "/tmp/none.csv")
        self.assertFalse(result)


class TestGetGoogleSheetsService(unittest.TestCase):

    @patch("utils.load.build")
    @patch("utils.load.Credentials.from_service_account_file")
    def test_returns_service(self, mock_creds, mock_build):
        mock_creds.return_value = Mock()
        mock_build.return_value = Mock()
        service = get_google_sheets_service("fake.json")
        self.assertIsNotNone(service)

    def test_missing_file_returns_none(self):
        service = get_google_sheets_service("tidak_ada.json")
        self.assertIsNone(service)


class TestSaveToGoogleSheets(unittest.TestCase):

    @patch("utils.load.get_google_sheets_service")
    def test_successful_save(self, mock_get_service):
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.spreadsheets().values().clear().execute.return_value = {}
        mock_service.spreadsheets().values().update().execute.return_value = {"updatedRows": 2}

        result = save_to_google_sheets(sample_df(), "fake_id", "fake.json")
        self.assertTrue(result)

    @patch("utils.load.get_google_sheets_service")
    def test_service_none_returns_false(self, mock_get_service):
        mock_get_service.return_value = None
        result = save_to_google_sheets(sample_df(), "fake_id", "fake.json")
        self.assertFalse(result)

    def test_empty_df_returns_false(self):
        result = save_to_google_sheets(pd.DataFrame(), "fake_id")
        self.assertFalse(result)

    def test_none_df_returns_false(self):
        result = save_to_google_sheets(None, "fake_id")
        self.assertFalse(result)

    def test_empty_spreadsheet_id_returns_false(self):
        result = save_to_google_sheets(sample_df(), "")
        self.assertFalse(result)


class TestGetPostgresEngine(unittest.TestCase):

    @patch("utils.load.create_engine")
    def test_returns_engine(self, mock_create_engine):
        mock_create_engine.return_value = Mock()
        engine = get_postgres_engine("postgresql://user:pass@localhost/db")
        self.assertIsNotNone(engine)

    @patch("utils.load.create_engine")
    def test_exception_returns_none(self, mock_create_engine):
        mock_create_engine.side_effect = Exception("Error")
        engine = get_postgres_engine("bad_url")
        self.assertIsNone(engine)


class TestSaveToPostgreSQL(unittest.TestCase):

    @patch("utils.load.get_postgres_engine")
    def test_successful_save(self, mock_get_engine):
        mock_engine = MagicMock()
        mock_get_engine.return_value = mock_engine
        with patch("pandas.DataFrame.to_sql") as mock_to_sql:
            mock_to_sql.return_value = None
            result = save_to_postgres(sample_df(), "postgresql://fake")
            self.assertTrue(result)

    @patch("utils.load.get_postgres_engine")
    def test_engine_none_returns_false(self, mock_get_engine):
        mock_get_engine.return_value = None
        result = save_to_postgres(sample_df(), "postgresql://fake")
        self.assertFalse(result)

    def test_empty_df_returns_false(self):
        result = save_to_postgres(pd.DataFrame(), "postgresql://fake")
        self.assertFalse(result)

    def test_none_df_returns_false(self):
        result = save_to_postgres(None, "postgresql://fake")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()