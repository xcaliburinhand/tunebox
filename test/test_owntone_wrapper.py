""" Test the owntone api wrapper """

import unittest
from tunebox import owntone_wrapper
import asyncio


class TestOwnToneWrapper(unittest.TestCase):
    def test_current_status(self):
        """ Test the status of the player """
        owntone = owntone_wrapper.Owntone("127.0.0.1", "3689")
        state = asyncio.run(owntone.player_state())
        assert state == "stop"
        assert not asyncio.run(owntone.playing)
