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


if __name__ == '__main__':
    unittest.main()
