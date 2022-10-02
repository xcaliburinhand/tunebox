import sys
import os
import time
import logging
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import board
from adafruit_seesaw.seesaw import Seesaw
import glob
from tunebox import display_image, state_machine, weather

logger = logging.getLogger('tunebox')

seesaw = Seesaw(board.I2C(), addr=0x30)


class Key:
    def __init__(self, key_number, _callback) -> None:
        self._pixelnum = key_number - 1
        self._pressed = _callback
        tbstate = state_machine.TuneboxState()
        tbstate.key_pixels[self._pixelnum] = 0x000000

    def press(self):
        tbstate = state_machine.TuneboxState()
        tbstate.key_pixels[self._pixelnum] = 0x4682B4
        self._pressed()
        tbstate.key_pixels[self._pixelnum] = 0x000000

    def _set_color(self, color_hex):
        tbstate = state_machine.TuneboxState()
        tbstate.key_pixels[self._num] = color_hex

    color = property(fset=_set_color)


def signal_handler(sig, frame):
    """ gracefully shutdown on signal """
    GPIO.cleanup()
    sys.exit(0)


def keyboard_handler(channel):
    """ handle keyboard key press / release """
    seesaw.get_GPIO_interrupt_flag()
    key_states = seesaw.digital_read_bulk(240)

    # nothing pressed, interrupt from key release
    if key_states == 240:
        return

    tbstate = state_machine.TuneboxState()
    tbstate.keys[key_states].press()


def weather_handler(tbstate):
    """ update forecast daily """
    tbstate.forecast = weather.Weather(
        tbstate.config["weather"]["city"],
        tbstate.config["weather"]["country"]
    )
    while True:
        tbstate.forecast.retrieve_forecast()
        tbstate.has_changed = True

        # sleep until 6 am tomorrow
        now = datetime.now()
        if now.hour < 12:
            time_until = (now.replace(hour=12, minute=0, second=0, microsecond=0) - now).total_seconds()  # noqa: E501
        else:
            # sleep until 6 am tomorrow
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
