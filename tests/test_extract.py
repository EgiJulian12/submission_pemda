import unittest
from unittest.mock import patch, Mock
import requests
from utils.extract import fetch_page, parse_products, scrape_main

SAMPLE_HTML = b"""
<html><body>
    <div class="collection-card">
        <div class="product-details">
        <h3 class="product-title">T-shirt 1</h3>
        <span class="price">$100.00</span>
        <p>Rating: 4.5 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
        </div>
    </div>
</body></html>
"""


class TestFetchPage(unittest.TestCase):

    def test_fetch_page_success(self):
        mock_session = Mock()
        mock_response = Mock()
        mock_response.content = b"<html>Test</html>"
        mock_response.raise_for_status = Mock()
        mock_session.get.return_value = mock_response

        result = fetch_page(mock_session, "https://example.com")
        self.assertEqual(result, b"<html>Test</html>")

    def test_fetch_page_request_exception(self):
        mock_session = Mock()
        mock_session.get.side_effect = requests.exceptions.RequestException("Error")

        result = fetch_page(mock_session, "https://example.com")
        self.assertIsNone(result)

    def test_fetch_page_unexpected_exception(self):
        mock_session = Mock()
        mock_session.get.side_effect = Exception("Unexpected")

        result = fetch_page(mock_session, "https://example.com")
        self.assertIsNone(result)


class TestParseProducts(unittest.TestCase):

    def test_returns_list(self):
        result = parse_products(SAMPLE_HTML)
        self.assertIsInstance(result, list)

    def test_correct_count(self):
        result = parse_products(SAMPLE_HTML)
        self.assertGreater(len(result), 0)

    def test_has_required_keys(self):
        result = parse_products(SAMPLE_HTML)
        required_keys = {"Title", "Price", "Rating", "Colors", "Size", "Gender", "Timestamp"}
        for product in result:
            self.assertTrue(required_keys.issubset(product.keys()))

    def test_title_extracted(self):
        result = parse_products(SAMPLE_HTML)
        titles = [p["Title"] for p in result]
        self.assertIn("T-shirt 1", titles)

    def test_none_input_returns_empty(self):
        result = parse_products(None)
        self.assertEqual(result, [])

    def test_timestamp_present(self):
        result = parse_products(SAMPLE_HTML)
        for product in result:
            self.assertIsNotNone(product.get("Timestamp"))


class TestScrapeMain(unittest.TestCase):

    @patch("utils.extract.fetch_page")
    @patch("utils.extract.requests.Session")
    def test_returns_list(self, mock_session, mock_fetch):
        mock_fetch.return_value = SAMPLE_HTML
        result = scrape_main()
        self.assertIsInstance(result, list)

    @patch("utils.extract.requests.Session")
    def test_request_exception_returns_none(self, mock_session_class):
        mock_session_class.side_effect = requests.exceptions.RequestException("Error")
        result = scrape_main()
        self.assertIsNone(result)

    @patch("utils.extract.fetch_page")
    @patch("utils.extract.requests.Session")
    def test_skips_failed_pages(self, mock_session, mock_fetch):
        mock_fetch.return_value = None
        result = scrape_main()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()