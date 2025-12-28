""" Test Weather """
import unittest
from tunebox import weather


class TestWeather(unittest.TestCase):
    """ Tests for Weather class """
    def test_coords(self):
        """ Test retrieve_coordinates """
        wthr = weather.Weather("New York", "US")
        coords = wthr.retrieve_coordinates("New York, US")

        # Use approximate matching since geocoding APIs may return slightly different coordinates
        want = [40.71455000000003, -74.00713999999994]
        self.assertAlmostEqual(coords[0], want[0], places=2)
        self.assertAlmostEqual(coords[1], want[1], places=2)

    def test_retrieve_forecast(self):
        """ Test retrieve_forecast """
        wthr = weather.Weather("New York", "US")
        wthr.retrieve_forecast()
        self.assertNotEqual(wthr.temperature["high"], "100")
        self.assertNotEqual(wthr.temperature["low"], "0")

    def test_merge_hourly(self):
        dset = {"time": ["2023-02-03T00:00","2023-02-03T01:00","2023-02-03T02:00","2023-02-03T03:00","2023-02-03T04:00","2023-02-03T05:00","2023-02-03T06:00","2023-02-03T07:00","2023-02-03T08:00","2023-02-03T09:00","2023-02-03T10:00","2023-02-03T11:00","2023-02-03T12:00","2023-02-03T13:00","2023-02-03T14:00","2023-02-03T15:00","2023-02-03T16:00","2023-02-03T17:00","2023-02-03T18:00","2023-02-03T19:00","2023-02-03T20:00","2023-02-03T21:00","2023-02-03T22:00","2023-02-03T23:00"], "weathercode": [3,3,2,0,0,2,3,1,0,0,1,2,3,3,1,3,3,0,0,0,0,0,0,0]}
        wthr = weather.Weather("New York", "US")
        result_set = wthr.merge_hourly(dset)
        self.assertEqual(len(result_set), 24)
        self.assertEqual(result_set[11], 2)
