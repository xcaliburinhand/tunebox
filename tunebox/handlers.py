import sys
import os
import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import glob
from tunebox import display_image, state_machine, weather


def signal_handler(sig, frame):
    """ gracefully shutdown on signal """
    GPIO.cleanup()
    sys.exit(0)


def keyboard_handler(channel):
    """ handle keyboard key press / release """
    pass


def weather_handler(tbstate):
    """ update forecast daily """
    tbstate.forecast = weather.Weather(
        tbstate.config["weather"]["city"],
        tbstate.config["weather"]["country"]
    )
    while True:
        tbstate.forecast.retrieve_forecast()

        # sleep until 6 am tomorrow
        now = datetime.now()
        time_until = (timedelta(hours=24) - (now - now.replace(hour=6, minute=0, second=0, microsecond=0))).total_seconds() % (24 * 3600)  # noqa: E501
        time.sleep(time_until)


def gather_icons():
    """ load icons into state """
    icons = {}
    for icon in glob.glob(
            os.path.join(os.path.dirname(__file__), "resources/icon-*.png")):
        icon_name = icon.split("icon-")[1].replace(".png", "")
        icons[icon_name] = display_image.Icon(icon)
    tbstate = state_machine.TuneboxState()
    tbstate.icons = icons
