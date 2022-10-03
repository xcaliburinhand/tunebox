""" Simplify owntone related functions """
import logging
import pyforked_daapd as daapd
import aiohttp
import asyncio
import websocket
import _thread as thread
from threading import Thread
from tunebox import keypress_routines, state_machine

logger = logging.getLogger('tunebox')


class Owntone:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port

    async def player_state(self):
        session = aiohttp.ClientSession()
        srv = daapd.ForkedDaapdAPI(session, self.host, self.port, "")
        player = await srv.get_request(endpoint="player")
        await session.close()
        return player["state"]

    async def now_playing(self):
        session = aiohttp.ClientSession()
        srv = daapd.ForkedDaapdAPI(session, self.host, self.port, "")
        track = await srv.get_current_queue_item()
        await session.close()
        return {"artist": track["artist"], "title": track["title"]}

    async def get_playing_state(self):
        return await self.player_state() == "playing"

    async def toggle_playback(self):
        session = aiohttp.ClientSession()
        srv = daapd.ForkedDaapdAPI(session, self.host, self.port, "")
        await srv.toggle_playback()
        await session.close()

    async def next_track(self):
        session = aiohttp.ClientSession()
        srv = daapd.ForkedDaapdAPI(session, self.host, self.port, "")
        await srv.next_track()
        await session.close()

    playing = property(get_playing_state)


ot = Owntone(
    state_machine.TuneboxState().DAAPD_HOST,
    state_machine.TuneboxState().DAAPD_PORT
)


def ws_open(ws):
    def run(*args):
        ws.send("{\"notify\": [\"player\"]}")
        tbstate = state_machine.TuneboxState()
        tbstate.keys[224].pressed = keypress_routines.toggle_playback
        tbstate.keys[224].color = 0x000044
        tbstate.keys[208].pressed = keypress_routines.next_track
    thread.start_new_thread(run, ())


def ws_error(ws, err):
    logger.error("owntone ws error encountered: ", err)


def ws_message(ws, message):
    ot_state = asyncio.run(ot.player_state())
    playing = ot_state == "play"
    logger.info(ot_state)
    playing_track_info = asyncio.run(ot.now_playing())
    logger.info(playing_track_info)
    tbstate = state_machine.TuneboxState()
    if tbstate.now_playing != playing_track_info or tbstate.player_playing != playing:
        tbstate.player_playing = playing
        tbstate.now_playing = playing_track_info
        tbstate.has_changed = True
        if playing:
            tbstate.key_pixels[0] = 0x009900
            tbstate.key_pixels[1] = 0x999900
        else:
            tbstate.key_pixels[0] = 0x990000
            tbstate.key_pixels[1] = 0x000000


def connect_socket():
    ws = websocket.WebSocketApp(
        "ws://localhost:3688/",
        on_error=ws_error,
        on_message=ws_message,
        header={"Sec-WebSocket-Protocol": "notify"}
    )
    ws.on_open = ws_open
    t = Thread(target=ws.run_forever)
    t.start()
