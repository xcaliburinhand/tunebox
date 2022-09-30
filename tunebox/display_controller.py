""" Tunebox display controller script """
import logging
from threading import Thread
import time
from inky.auto import auto
from tunebox import display_image, state_machine

logger = logging.getLogger('tunebox')


class TuneboxDisplayController(Thread):
    REFRESH_CYCLE = 60

    def __new__(cls):
        """ create new singleton object """
        if not hasattr(cls, 'instance'):
            cls.instance = super(TuneboxDisplayController, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """ kick off into the background """
        self.display = auto()
        self.tbstate = state_machine.TuneboxState()
        thread = Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            if self.tbstate.has_changed:
                self.update_display()
                self.tbstate.has_changed = False
            time.sleep(self.REFRESH_CYCLE)

    def update_display(self):
        """ display an updated image """
        img = display_image.Image()

        img.forecast = self.tbstate.forecast

        icon = self.tbstate.icons[self.tbstate.forecast.conditions]
        if self.tbstate.forecast.conditions == "sun":
            icon.recolor()
        img.draw_forecast_conditions(icon)

        self.display.set_image(img.generate())
        self.display.show()
