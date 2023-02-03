""" Tunebox Weather """

from datetime import datetime
import geocoder
import requests
import json
import logging

logger = logging.getLogger('tunebox')


class Weather:
    """ Weather forecast for a location """
    def __init__(self, city, countrycode):
        self.location_string = f"{city}, {countrycode}"
        self.conditions = "unknown"
        self.temperature = {
            "low": "0",
            "high": "100"
        }
        self.date = datetime(1900, 1, 1)

    def retrieve_coordinates(self, location):
        """ Convert a city name and country code to latitude and longitude """
        geocode = geocoder.arcgis(location)
        coords = geocode.latlng
        return coords

    def convert_skycon(self, skycon):
        """ Convert a skycon to a weather type """
        skycon_map = {
            "snow": ["snow-icon", "sleet-icon"],
            "rain": ["rain-icon"],
            "cloud": ["fog-icon", "cloudy-icon"],
            "partly-cloudy": ["partly-cloudy-day-icon",
                              "partly-cloudy-night-icon"],
            "sun": ["clear-day-icon", "clear-night-icon"],
            "storm": [],
            "wind": ["wind-icon"]
        }
        for key, value in skycon_map.items():
            if skycon in value:
                return key

    def convert_wmo(self, wmo):
        """ Convert wmo to a weather type
        https://open-meteo.com/en/docs#api-documentation """
        wmo_map = {
            "partly-cloudy": [1, 2],
            "cloud": [3],
            "sun": [0],
            "rain": [51, 53, 55, 61, 63, 65],
            "snow": [71, 73, 75]
        }
        for key, value in wmo_map.items():
            if wmo in value:
                return key
        logger.info(f'Weather wmo {wmo} unknown')
        return "unknown"

    def retrieve_forecast(self):
        """ Query open meteo for weather forecast """
        coords = self.retrieve_coordinates(self.location_string)

        res = requests.get(
            f"https://api.open-meteo.com/v1/gfs?latitude={coords[0]:.4f}&longitude={coords[1]:.4f}&models=gfs_hrrr&daily=weathercode,temperature_2m_max,temperature_2m_min&current_weather=true&temperature_unit=fahrenheit&timezone=America%2FNew_York"  # noqa: E501
        )

        if res.status_code == 200:
            gfs = json.loads(res.content)
            self.temperature["low"] = gfs['daily']['temperature_2m_min'][0]
            self.temperature["high"] = gfs['daily']['temperature_2m_max'][0]
            self.conditions = self.convert_wmo(
                gfs['daily']['weathercode'][0]
            )
            self.date = datetime.now()
