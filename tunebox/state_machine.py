import tomli


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
