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
        found = list(filter(lambda plist: plist['name'] == plistname, plists))
        return found

    playing = property(get_playing_state)
