""" Test the owntone api wrapper """

import unittest
import logging
from unittest.mock import patch, AsyncMock, MagicMock
from tunebox import owntone_wrapper
import asyncio

logging.basicConfig(level=logging.DEBUG)


class TestOwnToneWrapper(unittest.TestCase):
    @patch('tunebox.owntone_wrapper.daapd.ForkedDaapdAPI')
    @patch('tunebox.owntone_wrapper.aiohttp.ClientSession')
    def test_current_status(self, mock_session_class, mock_daapd_class):
        """ Test the status of the player """
        # Mock the API response
        mock_session = MagicMock()
        mock_session.close = AsyncMock()
        mock_session_class.return_value = mock_session
        
        mock_daapd_instance = MagicMock()
        mock_daapd_class.return_value = mock_daapd_instance
        mock_daapd_instance.get_request = AsyncMock(return_value={"state": "stop"})
        
        ot = owntone_wrapper.Owntone("127.0.0.1", "3689")
        state = asyncio.run(ot.player_state())
        assert state == "stop"
        playing = asyncio.run(ot.playing)
        assert not playing

    @patch('tunebox.owntone_wrapper.daapd.ForkedDaapdAPI')
    @patch('tunebox.owntone_wrapper.aiohttp.ClientSession')
    def test_search_playlist(self, mock_session_class, mock_daapd_class):
        """ Test playlist search """
        # Mock the API response
        mock_session = MagicMock()
        mock_session.close = AsyncMock()
        mock_session_class.return_value = mock_session
        
        mock_daapd_instance = MagicMock()
        mock_daapd_class.return_value = mock_daapd_instance
        mock_daapd_instance.get_playlists = AsyncMock(return_value=[
            {"name": "Played", "id": 1},
            {"name": "Other", "id": 2}
        ])
        
        owntone = owntone_wrapper.Owntone("127.0.0.1", "3689")
        found = asyncio.run(owntone.playlist_search("Played"))
        assert found[0]["name"] == "Played"
