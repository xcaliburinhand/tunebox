""" Test the functionality of the state """

import unittest
from tunebox import state_machine


class TestStateMachine(unittest.TestCase):
    def test_state_singleton(self):
        """ Test state consistency """
        tbstate = state_machine.TuneboxState()
        tbstate.mock = "test"

        tbstate2 = state_machine.TuneboxState()
        assert tbstate == tbstate2
        assert tbstate.mock == tbstate2.mock
