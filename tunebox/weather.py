""" Tunebox Weather """

import geocoder
import requests
from bs4 import BeautifulSoup


class Weather:
    """ Weather forecast for a location """
    def __init__(self, city, countrycode):
        self.location_string = f"{city}, {countrycode}"
        self.conditions = "sun"
        self.temperature = {
            "low": "0",
            "high": "100"
        }

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
            "cloud": ["fog-icon", "cloudy-icon", "partly-cloudy-day-icon",
                      "partly-cloudy-night-icon"],
            "sun": ["clear-day-icon", "clear-night-icon"],
            "storm": [],
            "wind": ["wind-icon"]
        }
        for key, value in skycon_map.items():
            if skycon in value:
                return key

    def retrieve_forecast(self, location):
        """ Query Dark Sky (https://darksky.net/) to scrape
        weather forecast """
        coords = self.retrieve_coordinates(location)

        coords_str = ",".join([str(c) for c in coords])
        res = requests.get(f"https://darksky.net/forecast/{coords_str}/us12/en")

        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "lxml")
            days = soup.find_all("a", "day")
            self.temperature["low"] = days[0].find("span", "minTemp").text
            self.temperature["high"] = days[0].find("span", "maxTemp").text
            self.conditions = self.convert_skycon(days[0].find("span", "skycon").img["class"][0])
