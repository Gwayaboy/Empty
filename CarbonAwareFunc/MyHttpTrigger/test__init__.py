import unittest
from __init__ import main
from unittest.mock import patch
from flask import Flask, jsonify

app = Flask(__name__)

def main(req, data):
    # ...
    with app.app_context():
        
        should_turn_on = data["data"][0]["intensity"]["actual"] < 100
        response_data = {"ShouldTurnOn": should_turn_on}
        return jsonify(response_data)

class TestMyHttpTrigger(unittest.TestCase):

    def test_main_actual_less_than_100(self):
        # Arrange
        req = None
        mock_data = {"data": [{"from": "2023-07-20T09:30Z", "to": "2023-07-20T10:00Z", "intensity": {"forecast": 179, "actual": 50, "index": "moderate"}}]}

        # Act
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_data
            response = main(req, mock_data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["ShouldTurnOn"], True)

    def test_main_actual_greater_than_100(self):
        # Arrange
        req = None
        mock_data = {"data": [{"from": "2023-07-20T09:30Z", "to": "2023-07-20T10:00Z", "intensity": {"forecast": 179, "actual": 150, "index": "moderate"}}]}

        # Act
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_data
            response = main(req, mock_data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["ShouldTurnOn"], False)