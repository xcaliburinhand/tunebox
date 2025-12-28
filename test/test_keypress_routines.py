""" Test the functionality of keypress routines """

import unittest
# Import test setup to mock hardware dependencies before importing tunebox modules
import test.test_setup  # noqa: F401
from unittest.mock import patch, AsyncMock
import time
from tunebox import keypress_routines, state_machine


class TestKeypressRoutines(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        # Reset state to ensure clean tests
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "none"
        tbstate.mode_timeout = 0
        tbstate.config = {
            "favorites": {
                "playlist": "TestPlaylist",
                "headphone_output": "TestHeadphones",
                "speaker_output": "TestSpeaker"
            }
        }
        # Initialize key_pixels as a list we can check
        tbstate.key_pixels = [None] * 4

    @patch('tunebox.keypress_routines.ot')
    def test_cycle_mode_none_to_remote_speaker(self, mock_ot):
        """Test cycling from none to remote_speaker mode"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "none"
        tbstate.mode_timeout = time.time() + 60  # Set future timeout so check_mode_timeout doesn't reset
        mock_ot.output_search = AsyncMock(return_value=[])
        
        keypress_routines.cycle_mode()
        
        assert tbstate.mode == "remote_speaker"
        assert tbstate.mode_timeout > time.time()

    @patch('tunebox.keypress_routines.ot')
    def test_cycle_mode_remote_speaker_to_headphones(self, mock_ot):
        """Test cycling from remote_speaker to headphones mode"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "remote_speaker"
        tbstate.mode_timeout = time.time() + 60  # Set future timeout so check_mode_timeout doesn't reset
        mock_ot.output_search = AsyncMock(return_value=[])
        
        keypress_routines.cycle_mode()
        
        assert tbstate.mode == "headphones"

    @patch('tunebox.keypress_routines.ot')
    def test_cycle_mode_headphones_to_playlist(self, mock_ot):
        """Test cycling from headphones to playlist mode"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "headphones"
        tbstate.mode_timeout = time.time() + 60  # Set future timeout so check_mode_timeout doesn't reset
        mock_ot.output_search = AsyncMock(return_value=[])
        
        keypress_routines.cycle_mode()
        
        assert tbstate.mode == "playlist"

    @patch('tunebox.keypress_routines.ot')
    def test_cycle_mode_playlist_to_none(self, mock_ot):
        """Test cycling from playlist back to none mode"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "playlist"
        tbstate.mode_timeout = time.time() + 60  # Set future timeout so check_mode_timeout doesn't reset
        mock_ot.output_search = AsyncMock(return_value=[])
        
        keypress_routines.cycle_mode()
        
        assert tbstate.mode == "none"

    @patch('tunebox.keypress_routines.ot')
    def test_cycle_mode_sets_timeout(self, mock_ot):
        """Test that cycling mode sets a 2-minute timeout"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "none"
        tbstate.mode_timeout = time.time() + 60  # Set future timeout so check_mode_timeout doesn't reset
        current_time = time.time()
        mock_ot.output_search = AsyncMock(return_value=[])
        
        keypress_routines.cycle_mode()
        
        # Timeout should be approximately 2 minutes (120 seconds) from now
        expected_timeout = current_time + 120
        assert abs(tbstate.mode_timeout - expected_timeout) < 2  # Allow 2 second tolerance

    @patch('tunebox.keypress_routines.ot')
    def test_update_output_colors_headphones_available_enabled(self, mock_ot):
        """Test output color update for headphones when available and enabled"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "headphones"
        # Create a list that we can check
        pixel_values = [None] * 4
        tbstate.key_pixels = pixel_values
        mock_ot.output_search = AsyncMock(return_value=[{"selected": True}])
        
        keypress_routines.update_output_colors()
        
        # Should set bright purple (0x800080)
        assert pixel_values[3] == 0x800080

    @patch('tunebox.keypress_routines.ot')
    def test_update_output_colors_headphones_available_disabled(self, mock_ot):
        """Test output color update for headphones when available but disabled"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "headphones"
        pixel_values = [None] * 4
        tbstate.key_pixels = pixel_values
        mock_ot.output_search = AsyncMock(return_value=[{"selected": False}])
        
        keypress_routines.update_output_colors()
        
        # Should set dim purple (0x100010)
        assert pixel_values[3] == 0x100010

    @patch('tunebox.keypress_routines.ot')
    def test_update_output_colors_headphones_unavailable(self, mock_ot):
        """Test output color update for headphones when unavailable"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "headphones"
        pixel_values = [None] * 4
        tbstate.key_pixels = pixel_values
        mock_ot.output_search = AsyncMock(return_value=[])
        
        keypress_routines.update_output_colors()
        
        # Should set no color (0x000000)
        assert pixel_values[3] == 0x000000

    @patch('tunebox.keypress_routines.ot')
    def test_update_output_colors_remote_speaker_available_enabled(self, mock_ot):
        """Test output color update for remote speaker when available and enabled"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "remote_speaker"
        pixel_values = [None] * 4
        tbstate.key_pixels = pixel_values
        mock_ot.output_search = AsyncMock(return_value=[{"selected": True}])
        
        keypress_routines.update_output_colors()
        
        # Should set bright cyan (0x00FF88)
        assert pixel_values[3] == 0x00FF88

    @patch('tunebox.keypress_routines.ot')
    def test_update_output_colors_remote_speaker_unavailable(self, mock_ot):
        """Test output color update for remote speaker when unavailable"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "remote_speaker"
        pixel_values = [None] * 4
        tbstate.key_pixels = pixel_values
        mock_ot.output_search = AsyncMock(return_value=[])
        
        keypress_routines.update_output_colors()
        
        # Should set no color (0x000000)
        assert pixel_values[3] == 0x000000

    def test_update_output_colors_no_config(self):
        """Test output color update when output not configured"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "headphones"
        pixel_values = [None] * 4
        tbstate.key_pixels = pixel_values
        tbstate.config["favorites"]["headphone_output"] = None
        
        keypress_routines.update_output_colors()
        
        # Should set no color (0x000000)
        assert pixel_values[3] == 0x000000

    @patch('tunebox.keypress_routines.ot')
    @patch('tunebox.keypress_routines.update_output_colors')
    def test_mode_action_headphones(self, mock_update_colors, mock_ot):
        """Test mode action for headphones mode"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "headphones"
        tbstate.mode_timeout = time.time() + 60  # Set future timeout so check_mode_timeout doesn't reset
        mock_ot.output_search = AsyncMock(return_value=[{"id": 1}])
        mock_ot.toggle_output = AsyncMock()
        
        keypress_routines.mode_action()
        
        mock_ot.output_search.assert_called_once()
        mock_ot.toggle_output.assert_called_once_with(1)
        mock_update_colors.assert_called_once()

    @patch('tunebox.keypress_routines.ot')
    @patch('tunebox.keypress_routines.update_output_colors')
    def test_mode_action_remote_speaker(self, mock_update_colors, mock_ot):
        """Test mode action for remote speaker mode"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "remote_speaker"
        tbstate.mode_timeout = time.time() + 60  # Set future timeout so check_mode_timeout doesn't reset
        mock_ot.output_search = AsyncMock(return_value=[{"id": 2}])
        mock_ot.toggle_output = AsyncMock()
        
        keypress_routines.mode_action()
        
        mock_ot.output_search.assert_called_once()
        mock_ot.toggle_output.assert_called_once_with(2)
        mock_update_colors.assert_called_once()

    @patch('tunebox.keypress_routines.ot')
    @patch('tunebox.keypress_routines.toggle_playback')
    def test_mode_action_playlist(self, mock_toggle, mock_ot):
        """Test mode action for playlist mode"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "playlist"
        tbstate.mode_timeout = time.time() + 60  # Set future timeout so check_mode_timeout doesn't reset
        mock_ot.playlist_search = AsyncMock(return_value=[{"id": 5}])
        mock_ot.shuffle_playlist = AsyncMock()
        
        keypress_routines.mode_action()
        
        mock_ot.playlist_search.assert_called_once_with("TestPlaylist")
        mock_ot.shuffle_playlist.assert_called_once_with(5)
        mock_toggle.assert_called_once()

    def test_mode_action_none(self):
        """Test mode action when mode is none"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "none"
        
        # Should return early without doing anything
        keypress_routines.mode_action()
        
        # No assertions needed, just verify it doesn't crash

    @patch('tunebox.keypress_routines.update_mode_colors')
    def test_check_mode_timeout_expired(self, mock_update_colors):
        """Test mode timeout check when timeout has expired"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "headphones"
        tbstate.mode_timeout = time.time() - 10  # Expired 10 seconds ago
        
        keypress_routines.check_mode_timeout()
        
        assert tbstate.mode == "none"
        assert tbstate.mode_timeout == 0
        mock_update_colors.assert_called_once()

    @patch('tunebox.keypress_routines.update_mode_colors')
    def test_check_mode_timeout_not_expired(self, mock_update_colors):
        """Test mode timeout check when timeout has not expired"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "headphones"
        tbstate.mode_timeout = time.time() + 60  # 60 seconds in the future
        
        keypress_routines.check_mode_timeout()
        
        assert tbstate.mode == "headphones"  # Should not change
        mock_update_colors.assert_not_called()

    def test_check_mode_timeout_none_mode(self):
        """Test mode timeout check when already in none mode"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "none"
        tbstate.mode_timeout = time.time() - 10
        
        keypress_routines.check_mode_timeout()
        
        assert tbstate.mode == "none"  # Should remain none

    def test_update_mode_colors_none(self):
        """Test mode color update for none mode"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "none"
        pixel_values = [None] * 4
        tbstate.key_pixels = pixel_values
        
        keypress_routines.update_mode_colors()
        
        # Button 3 should be no color (0x000000)
        assert pixel_values[2] == 0x000000
        # Button 4 should be no color (0x000000)
        assert pixel_values[3] == 0x000000

    def test_update_mode_colors_playlist(self):
        """Test mode color update for playlist mode"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "playlist"
        pixel_values = [None] * 4
        tbstate.key_pixels = pixel_values
        
        keypress_routines.update_mode_colors()
        
        # Button 3 should be orange (0xFF8800)
        assert pixel_values[2] == 0xFF8800
        # Button 4 should be orange at lower intensity (0x332200)
        assert pixel_values[3] == 0x332200

    @patch('tunebox.keypress_routines.ot')
    def test_mode_action_headphones_output_not_found(self, mock_ot):
        """Test mode action when headphones output is not found"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "headphones"
        mock_ot.output_search = AsyncMock(return_value=[])
        
        keypress_routines.mode_action()
        
        # Should not crash, just return early
        mock_ot.toggle_output.assert_not_called()

    @patch('tunebox.keypress_routines.ot')
    def test_mode_action_playlist_not_found(self, mock_ot):
        """Test mode action when playlist is not found"""
        tbstate = state_machine.TuneboxState()
        tbstate.mode = "playlist"
        mock_ot.playlist_search = AsyncMock(return_value=[])
        
        keypress_routines.mode_action()
        
        # Should not crash, just return early
        mock_ot.shuffle_playlist.assert_not_called()

