""" Test the owntone api wrapper """

import unittest
import logging
from tunebox import owntone_wrapper
import asyncio

logging.basicConfig(level=logging.DEBUG)


class TestOwnToneWrapper(unittest.TestCase):
    def test_current_status(self):
        """ Test the status of the player """
        ot = owntone_wrapper.Owntone("127.0.0.1", "3689")
        state = asyncio.run(ot.player_state())
        assert state == "stop"
        assert not asyncio.run(ot.playing)

    def test_search_playlist(self):
        owntone = owntone_wrapper.Owntone("127.0.0.1", "3689")
        found = asyncio.run(owntone.playlist_search("Played"))
        assert found[0]["name"] == "Played"
