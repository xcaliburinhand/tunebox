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
    asyncio.run(ot.toggle_playback())


def next_track():
    asyncio.run(ot.next_track())
