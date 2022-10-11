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
    logger.debug("queueing rocking playlist")
    plist = asyncio.run(ot.playlist_search("Rocking"))
    asyncio.run(ot.shuffle_playlist(plist[0]["id"]))
    tbstate = state_machine.TuneboxState()
    tbstate.keys[0x70].color = 0x000033
    toggle_playback()
