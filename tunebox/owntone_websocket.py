import logging
import asyncio
import websocket
import json
import _thread as thread
from threading import Thread
from tunebox import keypress_routines, owntone_wrapper, state_machine

logger = logging.getLogger('tunebox')

ot = owntone_wrapper.Owntone(
    state_machine.TuneboxState().DAAPD_HOST,
    state_machine.TuneboxState().DAAPD_PORT
)


def ws_open(ws):
    def run(*args):
        ws.send("{\"notify\": [\"player\",\"outputs\"]}")
        tbstate = state_machine.TuneboxState()
        tbstate.keys[0xe0].pressed = keypress_routines.toggle_playback
        tbstate.keys[0xd0].pressed = keypress_routines.next_track
        tbstate.keys[0xb0].pressed = keypress_routines.cycle_mode
        tbstate.keys[0x70].pressed = keypress_routines.mode_action
        # Initialize mode colors
        keypress_routines.update_mode_colors()
    thread.start_new_thread(run, ())


def ws_error(ws, err):
    logger.error("owntone ws error encountered: ", err)


def ws_message(ws, message):
    """Process push notifications from Owntone server"""
    logger.debug("Owntone websocket message received: %s", message)
    message_type = json.loads(message)["notify"]
    if "player" in message_type:
        player_notification()
    if "outputs" in message_type:
        outputs_notification()


def player_notification():
    """Process push notification for player"""
    ot_state = asyncio.run(ot.player_state())
    playing = ot_state == "play"
    logger.info(ot_state)
    playing_track_info = asyncio.run(ot.now_playing())
    logger.info(playing_track_info)
    tbstate = state_machine.TuneboxState()
    if tbstate.now_playing != playing_track_info or tbstate.player_playing != playing:  # noqa:E501
        tbstate.player_playing = playing
        tbstate.now_playing = playing_track_info
        tbstate.has_changed = True
        if playing:
            tbstate.key_pixels[0] = 0x007700
            tbstate.key_pixels[1] = 0x775500
        else:
            tbstate.key_pixels[0] = 0x770000
            tbstate.key_pixels[1] = 0x000000


def outputs_notification():
    """Process push notification for outputs"""
    # Use the shared function from keypress_routines to update output-based colors
    keypress_routines.update_output_colors()


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
