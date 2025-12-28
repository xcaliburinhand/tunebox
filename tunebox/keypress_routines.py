""" Bunch of routines that can be assigned to keys """

import logging
import asyncio
import time
from tunebox import owntone_wrapper, state_machine

DAAPD_HOST = "127.0.0.1"
DAAPD_PORT = "3689"


logger = logging.getLogger('tunebox')

ot = owntone_wrapper.Owntone(
    state_machine.TuneboxState().DAAPD_HOST,
    state_machine.TuneboxState().DAAPD_PORT
)


def nothing():
    logger.debug("No keypress action")


def toggle_playback():
    logger.debug("sending playback toggle")
    asyncio.run(ot.toggle_playback())


def next_track():
    logger.debug("requesting next track")
    asyncio.run(ot.next_track())


def rocking_playlist():
    logger.debug("queueing favorite playlist")
    tbstate = state_machine.TuneboxState()
    playlist_name = tbstate.config["favorites"]["playlist"]
    plist = asyncio.run(ot.playlist_search(playlist_name))
    if len(plist) == 0:
        logger.debug(f"Playlist {playlist_name} not found")
        return

    asyncio.run(ot.shuffle_playlist(plist[0]["id"]))
    tbstate = state_machine.TuneboxState()
    tbstate.keys[0x70].color = 0x000033
    toggle_playback()


def favorite_output():
    """Check if favorite output exists and toggle state"""
    tbstate = state_machine.TuneboxState()
    output_name = tbstate.config["favorites"]["output"]
    logger.debug("toggling output %s", output_name)

    output = asyncio.run(ot.output_search(output_name))
    if len(output) == 0:
        logger.debug("output %s not available", output_name)
        return

    asyncio.run(ot.toggle_output(output[0]["id"]))


def check_mode_timeout():
    """Check if mode timeout has expired and reset to none if needed"""
    tbstate = state_machine.TuneboxState()
    if tbstate.mode != "none" and time.time() > tbstate.mode_timeout:
        logger.debug("Mode timeout expired, resetting to none")
        tbstate.mode = "none"
        tbstate.mode_timeout = 0
        update_mode_colors()


def _get_output_state(output_name):
    """Get output state by name, returns (found, enabled) tuple"""
    output = asyncio.run(ot.output_search(output_name))
    if len(output) == 0:
        return (False, False)
    return (True, output[0]["selected"])


def _update_output_color(output_name, enabled_color, disabled_color):
    """Update button 4 color based on output state"""
    tbstate = state_machine.TuneboxState()
    found, enabled = _get_output_state(output_name)
    if not found:
        tbstate.key_pixels[3] = 0x000000
        return
    tbstate.key_pixels[3] = enabled_color if enabled else disabled_color
    logger.debug(f"Output {output_name} state: {enabled}")


def update_output_colors():
    """Update button 4 color based on output state for headphones or remote_speaker mode"""
    tbstate = state_machine.TuneboxState()
    
    if tbstate.mode == "headphones":
        output_name = tbstate.config["favorites"].get("headphone_output", None)
        if not output_name:
            tbstate.key_pixels[3] = 0x000000
            return
        _update_output_color(output_name, 0x800080, 0x100010)
    
    elif tbstate.mode == "remote_speaker":
        output_name = tbstate.config["favorites"].get("speaker_output", None)
        if not output_name:
            tbstate.key_pixels[3] = 0x000000
            return
        _update_output_color(output_name, 0x00FF88, 0x003322)


def cycle_mode():
    """Cycle through modes: none -> remote_speaker -> headphones -> playlist -> none"""
    tbstate = state_machine.TuneboxState()
    check_mode_timeout()
    
    mode_cycle = ["none", "remote_speaker", "headphones", "playlist"]
    current_index = mode_cycle.index(tbstate.mode) if tbstate.mode in mode_cycle else 0
    next_index = (current_index + 1) % len(mode_cycle)
    tbstate.mode = mode_cycle[next_index]
    
    # Set timeout to 2 minutes from now
    tbstate.mode_timeout = time.time() + 120
    
    logger.debug(f"Mode cycled to: {tbstate.mode}")
    update_mode_colors()
    
    # If entering headphones or remote_speaker mode, check output state
    if tbstate.mode in ["headphones", "remote_speaker"]:
        update_output_colors()


def update_mode_colors():
    """Update button colors based on current mode"""
    tbstate = state_machine.TuneboxState()
    
    # Button 3 (index 2) colors for each mode
    # Button 4 (index 3) colors at different intensity
    mode_colors = {
        "none": {
            "button3": 0x000000,  # no color
            "button4": 0x000000
        },
        "remote_speaker": {
            "button3": 0x00FF88  # cyan/teal
        },
        "headphones": {
            "button3": 0x800080   # purple
        },
        "playlist": {
            "button3": 0xFF8800,  # orange
            "button4": 0x332200   # orange at lower intensity
        }
    }
    
    colors = mode_colors.get(tbstate.mode, mode_colors["none"])
    tbstate.key_pixels[2] = colors["button3"]
    # Button 4 color will be updated by outputs_notification if in headphones/remote_speaker mode
    if tbstate.mode not in ["headphones", "remote_speaker"]:
        tbstate.key_pixels[3] = colors["button4"]


def _toggle_output(output_name, output_type):
    """Toggle output by name, returns True if successful"""
    if not output_name:
        logger.debug(f"{output_type} not configured")
        return False
    
    logger.debug(f"toggling {output_type} output {output_name}")
    output = asyncio.run(ot.output_search(output_name))
    if len(output) == 0:
        logger.debug(f"output {output_name} not available")
        return False
    
    asyncio.run(ot.toggle_output(output[0]["id"]))
    return True


def mode_action():
    """Perform action based on current mode"""
    tbstate = state_machine.TuneboxState()
    check_mode_timeout()
    
    if tbstate.mode == "none":
        logger.debug("Mode is none, no action")
        return
    
    if tbstate.mode == "headphones":
        output_name = tbstate.config["favorites"].get("headphone_output", None)
        if _toggle_output(output_name, "headphone"):
            update_output_colors()
    
    elif tbstate.mode == "remote_speaker":
        output_name = tbstate.config["favorites"].get("speaker_output", None)
        if _toggle_output(output_name, "speaker"):
            update_output_colors()
    
    elif tbstate.mode == "playlist":
        logger.debug("queueing favorite playlist")
        playlist_name = tbstate.config["favorites"]["playlist"]
        plist = asyncio.run(ot.playlist_search(playlist_name))
        if len(plist) == 0:
            logger.debug(f"Playlist {playlist_name} not found")
            return
        
        asyncio.run(ot.shuffle_playlist(plist[0]["id"]))
        toggle_playback()
