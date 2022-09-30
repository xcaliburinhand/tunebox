""" Bunch of routines that can be assigned to keys """

import logging
import aiohttp
import pyforked_daapd

DAAPD_HOST = "127.0.0.1"
DAAPD_PORT = "3689"


logger = logging.getLogger('tunebox')


def nothing():
    logger.debug("No keypress action")


def toggle_playback():
    session = aiohttp.ClientSession()
    daapd = pyforked_daapd.ForkedDaapdAPI(session, DAAPD_HOST, DAAPD_PORT, "")
    daapd.toggle_playback()


def next_track():
    session = aiohttp.ClientSession()
    daapd = pyforked_daapd.ForkedDaapdAPI(session, DAAPD_HOST, DAAPD_PORT, "")
    daapd.next_track()
