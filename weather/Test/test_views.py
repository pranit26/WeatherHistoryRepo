import unittest
from unittest.mock import patch, Mock
import datetime
import pandas as pd
from weather.views import registerUser,getHourlyData
from django.test import RequestFactory

mock_UserProfile = Mock()
mock_register_user_validator = Mock()


class WeatherTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()     


    @patch('weather.views.register_user_validator')
    @patch('weather.models.UserProfile')
    def test_registerUser(self, mock_UserProfile, mock_register_user_validator):
        mock_register_user_validator.return_value = (True, 'Valid data', {'username': 'testuser', 'password': 'Testpass1@','confirm_password':'Testpass1@'})
        mock_UserProfile.objects.filter.return_value = []

        request = self.factory.post('/register_user/', data={'username': 'testuser', 'password': 'Testpass1@'})

        with patch('weather.helpers.encrypt_AES_CBC', return_value='mockencryptedpassword'):
            response = registerUser(request)

        self.assertEqual(response.status_code, 201)
        self.assertIn("User registered successfully", response.data.get('message'))


    @patch('weather.views.openmeteo.weather_api')
    def test_getHourlyData_valid_data(self, mock_weather_api):
        mock_response = Mock()
        mock_response.Latitude.return_value = 52.52
        mock_response.Longitude.return_value = 13.41
        mock_response.Elevation.return_value = 100
        mock_response.Timezone.return_value = 'Europe/Berlin'
        mock_response.TimezoneAbbreviation.return_value = 'CET'
        mock_response.UtcOffsetSeconds.return_value = 3600
        mock_response.Hourly.return_value.Variables.return_value = [
            Mock(ValuesAsNumpy=lambda: [25.5, 26.0, 24.8]),
            Mock(ValuesAsNumpy=lambda: [0.0, 0.2, 0.1]),
            Mock(ValuesAsNumpy=lambda: [20, 30, 25])
        ]
        mock_weather_api.return_value = [mock_response]

        request_data = {
            "latitude": 52,
            "longitude": 31,
            "start_date": "2024-01-02",
            "end_date": "2024-01-16"
        }
        request = self.factory.post('/get_hourly_data/', data=request_data)
        response = getHourlyData(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Get_hourly_data", response.data)
        self.assertIn("temperature_2m", response.data["payload"])

