""" Test the functionality of the main handlers """

import unittest
from tunebox import handlers, state_machine


class TestHandlers(unittest.TestCase):
    def test_icon_gather(self):
        """ Test gathering icons """
        tbstate = state_machine.TuneboxState()

        handlers.gather_icons()
        assert len(tbstate.icons) > 0
