import unittest
from unittest.mock import patch
from datetime import datetime, timezone
from hello import app


class TestFlaskApp(unittest.TestCase):
    """Unit tests for Flask application endpoints."""

    def setUp(self) -> None:
        """Set up test client before each test."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_hello_endpoint(self) -> None:
        """Test the root endpoint returns hello message."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Hello, World!"})

    def test_health_endpoint(self) -> None:
        """Test the health check endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "healthy"})

    def test_greet_endpoint_valid_name(self) -> None:
        """Test greet endpoint with valid name."""
        response = self.client.get('/greet/mahi')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Hello, mahi!"})

    def test_greet_endpoint_empty_name(self) -> None:
        """Test greet endpoint with empty name."""
        response = self.client.get('/greet/ ')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_time_endpoint(self) -> None:
        """Test the time endpoint returns current server time."""
        mock_time = datetime(2025, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        with patch('hello.datetime') as mock_datetime:
            mock_datetime.now.return_value = mock_time
            mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
            response = self.client.get('/time')
        self.assertEqual(response.status_code, 200)
        self.assertIn("current_time", response.json)
        self.assertEqual(response.json["current_time"], "2025-01-15T12:00:00+00:00")

    # --- Tests for new endpoints ---

    def test_date_endpoint(self) -> None:
        """Test the date endpoint returns current date."""
        mock_time = datetime(2025, 6, 15, 8, 30, 0, tzinfo=timezone.utc)
        with patch('hello.datetime') as mock_datetime:
            mock_datetime.now.return_value = mock_time
            mock_datetime.side_effect = (
                lambda *args, **kwargs: datetime(*args, **kwargs)
            )
            response = self.client.get('/date')
        self.assertEqual(response.status_code, 200)
        self.assertIn("date", response.json)
        self.assertEqual(response.json["date"], "2025-06-15")

    def test_uuid_endpoint(self) -> None:
        """Test the uuid endpoint returns a valid UUID."""
        response = self.client.get('/uuid')
        self.assertEqual(response.status_code, 200)
        self.assertIn("uuid", response.json)
        # Validate UUID format (8-4-4-4-12 hex chars)
        import re
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}'
            r'-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
        )
        self.assertRegex(response.json["uuid"], uuid_pattern)

    def test_uuid_endpoint_uniqueness(self) -> None:
        """Test that successive UUID calls return different values."""
        resp1 = self.client.get('/uuid')
        resp2 = self.client.get('/uuid')
        self.assertNotEqual(resp1.json["uuid"], resp2.json["uuid"])

    def test_echo_endpoint_with_params(self) -> None:
        """Test echo endpoint returns query parameters."""
        response = self.client.get('/echo?name=alice&age=30')
        self.assertEqual(response.status_code, 200)
        self.assertIn("params", response.json)
        self.assertEqual(response.json["params"]["name"], "alice")
        self.assertEqual(response.json["params"]["age"], "30")

    def test_echo_endpoint_no_params(self) -> None:
        """Test echo endpoint with no query parameters."""
        response = self.client.get('/echo')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["params"], {})

    def test_random_endpoint_default(self) -> None:
        """Test random endpoint with default range."""
        response = self.client.get('/random')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("random", data)
        self.assertIn("min", data)
        self.assertIn("max", data)
        self.assertEqual(data["min"], 1)
        self.assertEqual(data["max"], 100)
        self.assertGreaterEqual(data["random"], 1)
        self.assertLessEqual(data["random"], 100)

    def test_random_endpoint_custom_range(self) -> None:
        """Test random endpoint with custom min and max."""
        response = self.client.get('/random?min=10&max=20')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data["min"], 10)
        self.assertEqual(data["max"], 20)
        self.assertGreaterEqual(data["random"], 10)
        self.assertLessEqual(data["random"], 20)

    def test_random_endpoint_invalid_range(self) -> None:
        """Test random endpoint where min > max returns error."""
        response = self.client.get('/random?min=50&max=10')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_random_endpoint_non_integer(self) -> None:
        """Test random endpoint with non-integer values."""
        response = self.client.get('/random?min=abc&max=10')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        self.assertEqual(
            response.json["error"],
            "min and max must be integers",
        )

    def test_reverse_endpoint(self) -> None:
        """Test reverse endpoint with valid text."""
        response = self.client.get('/reverse/hello')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data["original"], "hello")
        self.assertEqual(data["reversed"], "olleh")

    def test_reverse_endpoint_palindrome(self) -> None:
        """Test reverse endpoint with a palindrome."""
        response = self.client.get('/reverse/racecar')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data["original"], data["reversed"])

    def test_reverse_endpoint_empty_text(self) -> None:
        """Test reverse endpoint with whitespace-only text."""
        response = self.client.get('/reverse/ ')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)


if __name__ == '__main__':
    unittest.main()
