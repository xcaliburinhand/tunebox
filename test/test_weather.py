""" Test Weather """
import unittest
from tunebox import weather


class TestWeather(unittest.TestCase):
    """ Tests for Weather class """
    def test_coords(self):
        """ Test retrieve_coordinates """
        wthr = weather.Weather("New York", "US")
        coords = wthr.retrieve_coordinates("New York, US")

        want = [40.71455000000003, -74.00713999999994]
        self.assertEqual(coords, want)

    def test_retrieve_forecast(self):
        """ Test retrieve_forecast """
        wthr = weather.Weather("New York", "US")
        wthr.retrieve_forecast("New York, US")
        self.assertNotEqual(wthr.temperature["high"], "100")
        self.assertNotEqual(wthr.temperature["low"], "0")
