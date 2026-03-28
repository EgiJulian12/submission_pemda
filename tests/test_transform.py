import unittest
import pandas as pd
from utils.transform import (
    convert_price,
    convert_rating,
    convert_colors,
    convert_size,
    convert_gender,
    transform_data,
    exchange_rate,
)


class TestConvertPrice(unittest.TestCase):

    def test_valid_price(self):
        self.assertEqual(convert_price("$100.00"), 100.00 * exchange_rate)

    def test_price_unavailable(self):
        self.assertIsNone(convert_price("Price Unavailable"))

    def test_none_input(self):
        self.assertIsNone(convert_price(None))

    def test_empty_string(self):
        self.assertIsNone(convert_price(""))

    def test_price_with_comma(self):
        self.assertAlmostEqual(convert_price("$1,000.00"), 1000.0 * exchange_rate)

    def test_invalid_string(self):
        self.assertIsNone(convert_price("not a price"))


class TestConvertRating(unittest.TestCase):

    def test_valid_rating(self):
        self.assertEqual(convert_rating("4.8 / 5"), 4.8)

    def test_with_emoji(self):
        self.assertEqual(convert_rating("⭐ 4.8 / 5"), 4.8)

    def test_invalid_rating(self):
        self.assertIsNone(convert_rating("Invalid Rating / 5"))

    def test_not_rated(self):
        self.assertIsNone(convert_rating("Not Rated"))

    def test_none_input(self):
        self.assertIsNone(convert_rating(None))


class TestConvertColors(unittest.TestCase):

    def test_valid_colors(self):
        self.assertEqual(convert_colors("3 Colors"), 3)

    def test_none_input(self):
        self.assertIsNone(convert_colors(None))

    def test_invalid_input(self):
        self.assertIsNone(convert_colors("Colors"))


class TestConvertSize(unittest.TestCase):

    def test_valid_size(self):
        self.assertEqual(convert_size("Size: M"), "M")

    def test_none_input(self):
        self.assertIsNone(convert_size(None))

    def test_no_prefix(self):
        self.assertEqual(convert_size("XL"), "XL")


class TestConvertGender(unittest.TestCase):

    def test_valid_gender(self):
        self.assertEqual(convert_gender("Gender: Men"), "Men")

    def test_none_input(self):
        self.assertIsNone(convert_gender(None))

    def test_women(self):
        self.assertEqual(convert_gender("Gender: Women"), "Women")


class TestTransformData(unittest.TestCase):

    def sample_raw(self):
        return [
            {
                "Title": "T-shirt 2",
                "Price": "$102.12",
                "Rating": "⭐ 3.9 / 5",
                "Colors": "3 Colors",
                "Size": "Size: M",
                "Gender": "Gender: Women",
                "Timestamp": "2025-01-01T00:00:00",
            },
            {
                "Title": "Unknown Product",
                "Price": "$50.00",
                "Rating": "⭐ 4.0 / 5",
                "Colors": "2 Colors",
                "Size": "Size: S",
                "Gender": "Gender: Men",
                "Timestamp": "2025-01-01T00:00:00",
            },
            {
                "Title": "Hoodie 3",
                "Price": "Price Unavailable",
                "Rating": "Invalid Rating / 5",
                "Colors": "3 Colors",
                "Size": "Size: L",
                "Gender": "Gender: Unisex",
                "Timestamp": "2025-01-01T00:00:00",
            },
        ]

    def test_returns_dataframe(self):
        df = transform_data(self.sample_raw())
        self.assertIsInstance(df, pd.DataFrame)

    def test_removes_unknown_product(self):
        df = transform_data(self.sample_raw())
        self.assertNotIn("Unknown Product", df["Title"].values)

    def test_removes_null_rows(self):
        df = transform_data(self.sample_raw())
        self.assertFalse(df.isnull().any().any())

    def test_price_converted_to_rupiah(self):
        df = transform_data(self.sample_raw())
        expected = 102.12 * exchange_rate
        self.assertAlmostEqual(
            df[df["Title"] == "T-shirt 2"]["Price"].values[0],
            expected, places=1
        )

    def test_rating_is_float(self):
        df = transform_data(self.sample_raw())
        self.assertEqual(df["Rating"].dtype, "float64")

    def test_colors_is_int(self):
        df = transform_data(self.sample_raw())
        self.assertEqual(df["Colors"].dtype, "int64")

    def test_size_no_prefix(self):
        df = transform_data(self.sample_raw())
        for val in df["Size"].values:
            self.assertFalse(str(val).startswith("Size:"))

    def test_gender_no_prefix(self):
        df = transform_data(self.sample_raw())
        for val in df["Gender"].values:
            self.assertFalse(str(val).startswith("Gender:"))

    def test_none_input_returns_none(self):
        result = transform_data(None)
        self.assertIsNone(result)

    def test_empty_list_returns_none(self):
        self.assertIsNone(transform_data([]))


if __name__ == "__main__":
    unittest.main()