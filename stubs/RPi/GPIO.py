"""Stub module for RPi.GPIO - provides interface without hardware dependencies

This is a development stub that provides the same interface as RPi.GPIO
but without actual hardware control. Use this in development environments
where the actual RPi.GPIO library is not available.

On Raspberry Pi, install the real package: pip install RPi.GPIO
"""

import logging

logger = logging.getLogger(__name__)

# GPIO mode constants
BCM = 11
BOARD = 10

# GPIO direction constants
IN = 1
OUT = 0

# GPIO pull-up/pull-down constants
PUD_OFF = 0
PUD_DOWN = 1
PUD_UP = 2

# GPIO edge detection constants
RISING = 1
FALLING = 2
BOTH = 3

# GPIO state constants
HIGH = 1
LOW = 0

# GPIO function constants
SERIAL = 40
SPI = 41
I2C = 42
HARD_PWM = 43
UNKNOWN = -1


def setmode(mode):
    """Set the numbering mode used for the GPIO pins"""
    logger.debug(f"GPIO.setmode({mode}) - STUB: no-op")


def setup(channel, direction, initial=0, pull_up_down=PUD_OFF):
    """Set up a GPIO channel or list of channels"""
    logger.debug(f"GPIO.setup({channel}, {direction}, initial={initial}, pull_up_down={pull_up_down}) - STUB: no-op")


def output(channel, state):
    """Set the output state of a GPIO channel or list of channels"""
    logger.debug(f"GPIO.output({channel}, {state}) - STUB: no-op")


def input(channel):
    """Read the value of a GPIO channel"""
    logger.debug(f"GPIO.input({channel}) - STUB: returning LOW")
    return LOW


def cleanup(channel=None):
    """Clean up GPIO resources"""
    logger.debug(f"GPIO.cleanup({channel}) - STUB: no-op")


def add_event_detect(channel, edge, callback=None, bouncetime=None):
    """Enable edge detection events for a particular GPIO channel"""
    logger.debug(f"GPIO.add_event_detect({channel}, {edge}, callback={callback}, bouncetime={bouncetime}) - STUB: no-op")


def remove_event_detect(channel):
    """Remove edge detection for a particular GPIO channel"""
    logger.debug(f"GPIO.remove_event_detect({channel}) - STUB: no-op")


def event_detected(channel):
    """Returns True if an edge has occurred on a given GPIO channel"""
    logger.debug(f"GPIO.event_detected({channel}) - STUB: returning False")
    return False


def wait_for_edge(channel, edge, timeout=None):
    """Wait for an edge on a GPIO channel"""
    logger.debug(f"GPIO.wait_for_edge({channel}, {edge}, timeout={timeout}) - STUB: returning None")
    return None


def gpio_function(channel):
    """Return the current GPIO function (IN, OUT, PWM, SERIAL, I2C, SPI)"""
    logger.debug(f"GPIO.gpio_function({channel}) - STUB: returning UNKNOWN")
    return UNKNOWN


def setwarnings(flag):
    """Enable or disable warning messages"""
    logger.debug(f"GPIO.setwarnings({flag}) - STUB: no-op")

