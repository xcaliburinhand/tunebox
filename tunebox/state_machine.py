import tomli
from adafruit_seesaw import neopixel
import board
from adafruit_seesaw.seesaw import Seesaw

_NEOKEY1X4_NEOPIX_PIN = 3
_NEOKEY1X4_NUM_KEYS = 4

seesaw = Seesaw(board.I2C(), addr=0x30)


class TuneboxState(object):
    """ singleton object handling system state """

    DAAPD_HOST = "127.0.0.1"
    DAAPD_PORT = "3689"

    config = {
        "weather": {
            "city": "Philadelphia, PA",
            "country": "US"
        }
    }

    keys = []

    player_playing = False
    now_playing = {"artist": "", "title": ""}

    # provide signal that state has changed
    has_changed = False

    def __new__(cls):
        """ create new singleton object """
        if not hasattr(cls, 'instance'):
            cls.instance = super(TuneboxState, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        try:
            with open("/etc/tunebox/tunebox.toml", mode="rb") as fp:
                self.config = tomli.load(fp)
        except FileNotFoundError:
            pass

        self.key_pixels = neopixel.NeoPixel(
            seesaw,
            _NEOKEY1X4_NEOPIX_PIN,
            _NEOKEY1X4_NUM_KEYS,
            brightness=0.2,
            pixel_order=neopixel.GRB,
        )
