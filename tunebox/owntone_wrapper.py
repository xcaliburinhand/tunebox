""" Simplify owntone related functions """
import logging
import pyforked_daapd as daapd
import aiohttp

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

    async def shuffle_playlist(self, plistid):
        session = aiohttp.ClientSession()
        srv = daapd.ForkedDaapdAPI(session, self.host, self.port, "")
        await srv.clear_queue()
        await srv.add_to_queue(
            uris="library:playlist:{}".format(plistid),
            shuffle=True
        )
        await session.close()

    async def playlist_search(self, plistname):
        session = aiohttp.ClientSession()
        srv = daapd.ForkedDaapdAPI(session, self.host, self.port, "")
        plists = await srv.get_playlists()
        await session.close()
        found = list(filter(lambda plist: plist['name'].lower() == plistname.lower(), plists))
        return found

    async def output_search(self, outputname):
        """Find an output by name"""
        outputs = await self.get_outputs()
        found = list(
            filter(lambda output: output['name'].lower() == outputname.lower(), outputs)
        )
        return found

    async def get_outputs(self):
        """Retrieve a list of available outputs from Owntone server"""
        session = aiohttp.ClientSession()
        srv = daapd.ForkedDaapdAPI(session, self.host, self.port, "")
        outputs = await srv.get_request("outputs")
        await session.close()
        return outputs.get("outputs") if outputs else None

    async def toggle_output(self, output_id):
        """Toggle output state"""
        session = aiohttp.ClientSession()
        srv = daapd.ForkedDaapdAPI(session, self.host, self.port, "")
        status = await srv.put_request(endpoint=f"outputs/{output_id}/toggle")
        await session.close()
        if status != 204:
            logger.debug("Unable to change state of output %s", output_id)
        return status

    playing = property(get_playing_state)
