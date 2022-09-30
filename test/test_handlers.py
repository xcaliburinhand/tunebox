""" Test the functionality of the main handlers """

import unittest
from tunebox import handlers, keypress_routines, state_machine
import logging

logging.basicConfig(level=logging.DEBUG)


def key_press_callback():
    logger = logging.getLogger('tunebox')
    logger.info("PRESSED")


class TestHandlers(unittest.TestCase):
    def test_icon_gather(self):
        """ Test gathering icons """
        tbstate = state_machine.TuneboxState()

        handlers.gather_icons()
        assert len(tbstate.icons) > 0

    def test_key(self):
        key = handlers.Key(1, key_press_callback)
        key.press()

    def test_key_color(self):
        key = handlers.Key(2, keypress_routines.nothing)
        key.color = 0x00aa00
