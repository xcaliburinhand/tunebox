""" Test display image creator """

import logging
import os
import unittest
from PIL import Image
from tunebox import display_image

logging.basicConfig(level=logging.DEBUG)


class MockForecast:
    def __init__(self):
        self.conditions = "wind"
        self.temperature = {"high": "87", "low": "21"}


class TestDisplayImage(unittest.TestCase):
    """ Test classes in display_image """

    MOCK_FORECAST = MockForecast()

    def test_image_save(self):
        """ Test writing image to filesystem """
        img = display_image.Image()
        img.forecast = self.MOCK_FORECAST
        img.generate()
        img.save()

        bmp = Image.open('out.bmp')
        assert bmp.size[1] == 122
        assert bmp.getpixel((3, 3)) == 200

    def test_create_mask(self):
        icon = display_image.Icon(
            os.path.join(
                os.path.dirname(__file__),
                "../tunebox/resources/icon-snow.png"
            )
        )
        assert icon.mask.getpixel((20, 5)) == 255

    def test_draw_weather_icon(self):
        icon = display_image.Icon(
            os.path.join(
                os.path.dirname(__file__),
                "../tunebox/resources/icon-sun.png"
            )
        )
        icon.recolor()
        img = display_image.Image()
        img.draw_forecast_conditions(icon)
        assert img.img.getpixel((224, 6)) == 2
