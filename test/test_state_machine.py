""" Test the functionality of the state """

import unittest
from tunebox import state_machine


class TestStateMachine(unittest.TestCase):
    def test_state_singleton(self):
        """ Test state consistency """
        tbstate = state_machine.TuneboxState()
        tbstate.mock = "test"

        tbstate2 = state_machine.TuneboxState()
        assert tbstate == tbstate2
        assert tbstate.mock == tbstate2.mock

    def test_set_pixel(self):
        tbstate = state_machine.TuneboxState()
        tbstate.key_pixels[2] = 0x0F000F
        tbstate.key_pixels[0] = 0x050800

        tbstate = state_machine.TuneboxState()
        tbstate.key_pixels[1] = 0x4682B4
