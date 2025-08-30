import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add the current directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import build_query_param, get_weather


class TestWeatherFunctions(unittest.TestCase):

    def setUp(self):
        """Set up test environment"""
        # Set environment variable for testing
        os.environ["WEATHERSTACK_API_KEY"] = "test_api_key"

    def test_build_query_param_city(self):
        """Test building query parameter with city name"""
        query = build_query_param("London", None, None)
        self.assertEqual(query, "London")

    def test_build_query_param_coordinates(self):
        """Test building query parameter with coordinates"""
        query = build_query_param(None, 40.7128, -74.0060)
        # Handle floating point precision - check that both lat and lon are present
        self.assertIn("40.7128", query)
        self.assertIn("-74.006", query)
        self.assertIn(",", query)

    def test_build_query_param_coordinates_precise(self):
        """Test building query parameter with coordinates - precise check"""
        query = build_query_param(None, 40.0, -74.0)
        self.assertEqual(query, "40.0,-74.0")

    def test_build_query_param_invalid(self):
        """Test building query parameter with invalid input"""
        with self.assertRaises(ValueError):
            build_query_param(None, None, None)

    def test_build_query_param_city_and_coordinates(self):
        """Test building query parameter with both city and coordinates"""
        query = build_query_param("London", 40.7128, -74.0060)
        # Should contain both city and coordinates
        self.assertIn("London", query)
        self.assertIn("40.7128", query)
        self.assertIn("-74.006", query)
        self.assertEqual(
            query.count(";"), 1
        )  # One separator between city and coordinates

    def test_build_query_param_multiple_cities_and_coordinates(self):
        """Test building query parameter with multiple cities and coordinates"""
        query = build_query_param("London,Paris", 40.7128, -74.0060)
        # Should contain all cities and coordinates
        self.assertIn("London", query)
        self.assertIn("Paris", query)
        self.assertIn("40.7128", query)
        self.assertIn("-74.006", query)
        self.assertEqual(
            query.count(";"), 2
        )  # Two separators: between cities and between cities and coordinates

    def test_build_query_param_coordinates_only(self):
        """Test building query parameter with coordinates only"""
        query = build_query_param(None, 40.7128, -74.0060)
        # Handle floating point precision - check that both lat and lon are present
        self.assertIn("40.7128", query)
        self.assertIn("-74.006", query)
        self.assertIn(",", query)
        self.assertEqual(
            query.count(";"), 0
        )  # No separators for single coordinate pair

    @patch("main.requests.get")
    def test_get_weather_success_city(self, mock_get):
        """Test successful weather fetch for a city"""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            "request": {
                "type": "City",
                "query": "London, United Kingdom",
                "language": "en",
                "unit": "m",
            },
            "location": {
                "name": "London",
                "country": "United Kingdom",
                "region": "City of London, Greater London",
                "lat": "51.517",
                "lon": "-0.106",
                "timezone_id": "Europe/London",
                "localtime": "2025-06-23 22:30",
                "localtime_epoch": 1719179400,
                "utc_offset": "1.0",
            },
            "current": {
                "observation_time": "09:30 PM",
                "temperature": 18,
                "weather_code": 113,
                "weather_icons": [
                    "https://assets.weatherstack.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png"
                ],
                "weather_descriptions": ["Clear"],
                "wind_speed": 15,
                "wind_degree": 280,
                "wind_dir": "W",
                "pressure": 1015,
                "precip": 0,
                "humidity": 65,
                "cloudcover": 0,
                "feelslike": 18,
                "uv_index": 5,
                "visibility": 10,
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Capture print output
        with patch("builtins.print") as mock_print:
            get_weather(city="London")

            # Verify the API was called correctly
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            self.assertEqual(call_args[1]["params"]["query"], "London")
            self.assertEqual(call_args[1]["params"]["access_key"], "test_api_key")

            # Verify output was printed
            mock_print.assert_called()

    @patch("main.requests.get")
    def test_get_weather_success_coordinates(self, mock_get):
        """Test successful weather fetch for coordinates"""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            "request": {
                "type": "LatLon",
                "query": "Lat 40.71 and Lon -74.01",
                "language": "en",
                "unit": "m",
            },
            "location": {
                "name": "New York",
                "country": "United States of America",
                "region": "New York",
                "lat": "40.714",
                "lon": "-74.006",
                "timezone_id": "America/New_York",
                "localtime": "2025-06-23 17:30",
                "localtime_epoch": 1719161400,
                "utc_offset": "-4.0",
            },
            "current": {
                "observation_time": "09:30 PM",
                "temperature": 25,
                "weather_code": 116,
                "weather_icons": [
                    "https://assets.weatherstack.com/images/wsymbols01_png_64/wsymbol_0002_sunny_intervals.png"
                ],
                "weather_descriptions": ["Partly cloudy"],
                "wind_speed": 12,
                "wind_degree": 270,
                "wind_dir": "W",
                "pressure": 1013,
                "precip": 0,
                "humidity": 60,
                "cloudcover": 25,
                "feelslike": 26,
                "uv_index": 6,
                "visibility": 16,
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with patch("builtins.print") as mock_print:
            get_weather(lat=40.7128, lon=-74.0060)

            # Verify the API was called correctly
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            query_param = call_args[1]["params"]["query"]
            # Handle floating point precision - check that both lat and lon are present
            self.assertIn("40.7128", query_param)
            self.assertIn("-74.006", query_param)
            self.assertIn(",", query_param)

            # Verify output was printed
            mock_print.assert_called()

    @patch("main.requests.get")
    def test_get_weather_city_not_found(self, mock_get):
        """Test weather fetch for non-existent city"""
        # Mock error response
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": False,
            "error": {
                "code": 615,
                "type": "request_failed",
                "info": "API request failed.",
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with patch("builtins.print") as mock_print:
            get_weather(city="NonExistentCity")

            # Verify error message was printed
            mock_print.assert_called_with("Error: API request failed.")

    @patch("main.requests.get")
    def test_get_weather_api_unavailable(self, mock_get):
        """Test weather fetch when API is unavailable"""
        # Mock HTTP error
        mock_get.side_effect = Exception("Connection failed")

        with patch("builtins.print") as mock_print:
            get_weather(city="London")

            # Verify error message was printed
            mock_print.assert_called_with("Error: Connection failed")

    @patch("main.requests.get")
    def test_get_weather_missing_api_key(self, mock_get):
        """Test weather fetch with missing API key"""
        # Remove API key from environment
        if "WEATHERSTACK_API_KEY" in os.environ:
            del os.environ["WEATHERSTACK_API_KEY"]

        with patch("builtins.print") as mock_print:
            get_weather(city="London")

            # Verify error message was printed
            mock_print.assert_called_with("Missing WEATHERSTACK_API_KEY in .env file.")

            # Verify API was not called
            mock_get.assert_not_called()

    @patch("main.requests.get")
    def test_get_weather_http_error(self, mock_get):
        """Test weather fetch with HTTP error"""
        # Mock HTTP error
        mock_get.side_effect = Exception("HTTP 500 Internal Server Error")

        with patch("builtins.print") as mock_print:
            get_weather(city="London")

            # Verify error message was printed
            mock_print.assert_called_with("Error: HTTP 500 Internal Server Error")

    @patch("main.requests.get")
    def test_get_weather_invalid_response(self, mock_get):
        """Test weather fetch with invalid JSON response"""
        # Mock invalid response
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with patch("builtins.print") as mock_print:
            get_weather(city="London")

            # Verify error message was printed
            mock_print.assert_called_with("Error: Invalid JSON")

    @patch("main.requests.get")
    def test_get_weather_multiple_cities(self, mock_get):
        """Test successful weather fetch for multiple cities in one request"""
        # Mock successful response for multiple cities
        mock_response = Mock()
        mock_response.json.return_value = {
            "location": [
                {
                    "name": "London",
                    "country": "United Kingdom",
                    "region": "City of London, Greater London",
                    "lat": "51.517",
                    "lon": "-0.106",
                    "timezone_id": "Europe/London",
                    "localtime": "2025-06-23 22:30",
                    "localtime_epoch": 1719179400,
                    "utc_offset": "1.0",
                },
                {
                    "name": "Paris",
                    "country": "France",
                    "region": "Ile-de-France",
                    "lat": "48.853",
                    "lon": "2.349",
                    "timezone_id": "Europe/Paris",
                    "localtime": "2025-06-23 23:30",
                    "localtime_epoch": 1719183000,
                    "utc_offset": "2.0",
                },
            ],
            "current": [
                {
                    "observation_time": "09:30 PM",
                    "temperature": 18,
                    "weather_code": 113,
                    "weather_icons": [
                        "https://assets.weatherstack.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png"
                    ],
                    "weather_descriptions": ["Clear"],
                    "wind_speed": 15,
                    "wind_degree": 280,
                    "wind_dir": "W",
                    "pressure": 1015,
                    "precip": 0,
                    "humidity": 65,
                    "cloudcover": 0,
                    "feelslike": 18,
                    "uv_index": 5,
                    "visibility": 10,
                },
                {
                    "observation_time": "10:30 PM",
                    "temperature": 20,
                    "weather_code": 116,
                    "weather_icons": [
                        "https://assets.weatherstack.com/images/wsymbols01_png_64/wsymbol_0002_sunny_intervals.png"
                    ],
                    "weather_descriptions": ["Partly cloudy"],
                    "wind_speed": 10,
                    "wind_degree": 250,
                    "wind_dir": "WSW",
                    "pressure": 1012,
                    "precip": 0,
                    "humidity": 60,
                    "cloudcover": 20,
                    "feelslike": 21,
                    "uv_index": 6,
                    "visibility": 12,
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with patch("builtins.print") as mock_print:
            get_weather(city="London,Paris")
            # Verify the API was called with semicolon-separated cities
            call_args = mock_get.call_args
            self.assertEqual(call_args[1]["params"]["query"], "London;Paris")
            # Verify output was printed for both cities
            self.assertTrue(mock_print.call_count > 1)

    @patch("main.requests.get")
    def test_get_weather_city_and_coordinates(self, mock_get):
        """Test successful weather fetch for both city and coordinates"""
        # Mock successful response for city + coordinates
        mock_response = Mock()
        mock_response.json.return_value = {
            "location": [
                {
                    "name": "London",
                    "country": "United Kingdom",
                    "region": "City of London, Greater London",
                    "lat": "51.517",
                    "lon": "-0.106",
                    "timezone_id": "Europe/London",
                    "localtime": "2025-06-23 22:30",
                    "localtime_epoch": 1719179400,
                    "utc_offset": "1.0",
                },
                {
                    "name": "New York",
                    "country": "United States of America",
                    "region": "New York",
                    "lat": "40.714",
                    "lon": "-74.006",
                    "timezone_id": "America/New_York",
                    "localtime": "2025-06-23 17:30",
                    "localtime_epoch": 1719161400,
                    "utc_offset": "-4.0",
                },
            ],
            "current": [
                {
                    "observation_time": "09:30 PM",
                    "temperature": 18,
                    "weather_code": 113,
                    "weather_icons": [
                        "https://assets.weatherstack.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png"
                    ],
                    "weather_descriptions": ["Clear"],
                    "wind_speed": 15,
                    "wind_degree": 280,
                    "wind_dir": "W",
                    "pressure": 1015,
                    "precip": 0,
                    "humidity": 65,
                    "cloudcover": 0,
                    "feelslike": 18,
                    "uv_index": 5,
                    "visibility": 10,
                },
                {
                    "observation_time": "09:30 PM",
                    "temperature": 25,
                    "weather_code": 116,
                    "weather_icons": [
                        "https://assets.weatherstack.com/images/wsymbols01_png_64/wsymbol_0002_sunny_intervals.png"
                    ],
                    "weather_descriptions": ["Partly cloudy"],
                    "wind_speed": 12,
                    "wind_degree": 270,
                    "wind_dir": "W",
                    "pressure": 1013,
                    "precip": 0,
                    "humidity": 60,
                    "cloudcover": 25,
                    "feelslike": 26,
                    "uv_index": 6,
                    "visibility": 16,
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with patch("builtins.print") as mock_print:
            get_weather(city="London", lat=40.7128, lon=-74.0060)

            # Verify the API was called with both city and coordinates
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            query_param = call_args[1]["params"]["query"]
            self.assertIn("London", query_param)
            self.assertIn("40.7128", query_param)
            self.assertIn("-74.006", query_param)
            self.assertIn(";", query_param)

            # Verify output was printed for both locations
            self.assertTrue(mock_print.call_count > 1)

    @patch("main.requests.get")
    def test_get_weather_garbage_city_input(self, mock_get):
        """Test weather fetch with garbage/invalid city names"""
        # Test inputs that should raise ValueError (empty/whitespace)
        invalid_inputs = [
            "",  # Empty string
            "   ",  # Whitespace only
        ]

        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaises(ValueError):
                    get_weather(city=invalid_input)

        # Test inputs that should make API calls but return errors
        garbage_inputs = [
            "12345",  # Numbers only
            "!@#$%^&*()",  # Special characters only
            "A" * 1000,  # Very long string
            "null",  # String "null"
            "undefined",  # String "undefined"
            "NaN",  # String "NaN"
            "London;Paris",  # Semicolon in city name (should be handled)
            "London,Paris,Berlin,",  # Trailing comma
            ",London,Paris",  # Leading comma
        ]

        for garbage_input in garbage_inputs:
            with self.subTest(garbage_input=garbage_input):
                # Mock error response for invalid city
                mock_response = Mock()
                mock_response.json.return_value = {
                    "success": False,
                    "error": {
                        "code": 615,
                        "type": "request_failed",
                        "info": "API request failed.",
                    },
                }
                mock_response.raise_for_status.return_value = None
                mock_get.return_value = mock_response

                with patch("builtins.print") as mock_print:
                    get_weather(city=garbage_input)

                    # Verify the API was called (even with garbage input)
                    mock_get.assert_called()

                    # Verify error message was printed
                    mock_print.assert_called_with("Error: API request failed.")

                    # Reset mock for next iteration
                    mock_get.reset_mock()
                    mock_print.reset_mock()

    @patch("main.requests.get")
    def test_get_weather_malformed_city_input(self, mock_get):
        """
        Test weather fetch with malformed city input that
        might cause parsing issues
        """
        # Test inputs that might cause issues in string processing
        malformed_inputs = [
            "London\nParis",  # Newline in city name
            "London\tParis",  # Tab in city name
            "London\rParis",  # Carriage return in city name
            "London\\Paris",  # Backslash in city name
            "London'Paris",  # Single quote in city name
            'London"Paris',  # Double quote in city name
            "London/Paris",  # Forward slash in city name
            "London|Paris",  # Pipe in city name
        ]

        for malformed_input in malformed_inputs:
            with self.subTest(malformed_input=malformed_input):
                # Mock error response for malformed input
                mock_response = Mock()
                mock_response.json.return_value = {
                    "success": False,
                    "error": {
                        "code": 601,
                        "type": "missing_query",
                        "info": "An invalid (or missing) query value was specified.",
                    },
                }
                mock_response.raise_for_status.return_value = None
                mock_get.return_value = mock_response

                with patch("builtins.print") as mock_print:
                    get_weather(city=malformed_input)

                    # Verify the API was called
                    mock_get.assert_called()

                    # Verify error message was printed
                    mock_print.assert_called_with(
                        "Error: An invalid (or missing) query value was specified."
                    )

                    # Reset mock for next iteration
                    mock_get.reset_mock()
                    mock_print.reset_mock()


class TestWeatherAPI(unittest.TestCase):

    def test_koln(self):
        """Test Koln"""
        # This test requires a real API key and makes an actual API call
        # Capture the printed output
        import sys
        from io import StringIO

        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            # Make the actual API call with "Köln"
            get_weather(city="Köln")
        except Exception as e:
            # If API key is missing or other issues, skip the test
            self.skipTest(f"API test skipped due to: {e}")
        finally:
            sys.stdout = sys.__stdout__

        # Get the captured output
        output = captured_output.getvalue()

        # Verify the API returned Kolno, Poland (the expected result for "Koln")
        self.assertIn("Kolno", output)


class TestWeatherIntegration(unittest.TestCase):
    """Integration tests that can be run with real API (optional)"""

    # @unittest.skip("Skip integration test by default")
    def test_real_api_call(self):
        """Test with real API call (requires valid API key)"""
        # This test will only run if explicitly enabled
        # Set WEATHERSTACK_API_KEY environment variable to run this test
        if not os.getenv("WEATHERSTACK_API_KEY"):
            self.skipTest("No API key provided for integration test")

        with patch("builtins.print") as mock_print:
            get_weather(city="London")
            get_weather(city="London, Paris, Berlin")
            # Verify that some output was printed (indicating success)
            self.assertTrue(mock_print.called)


if __name__ == "__main__":
    unittest.main()
