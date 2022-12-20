""" Bunch of routines that can be assigned to keys """

import logging
import asyncio
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
