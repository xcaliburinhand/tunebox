"""Test setup - mock hardware dependencies before imports"""
import sys
from unittest.mock import MagicMock

# Mock RPi.GPIO before any imports
mock_gpio = MagicMock()
mock_gpio.BCM = 11
mock_gpio.IN = 1
mock_gpio.PUD_OFF = 0
mock_gpio.FALLING = 2
mock_gpio.setmode = MagicMock()
mock_gpio.setup = MagicMock()
mock_gpio.add_event_detect = MagicMock()
mock_gpio.cleanup = MagicMock()
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = mock_gpio

# Mock board module before any imports
mock_board = MagicMock()
mock_i2c = MagicMock()
mock_board.I2C = MagicMock(return_value=mock_i2c)
sys.modules['board'] = mock_board

# Mock adafruit_seesaw.seesaw.Seesaw
mock_seesaw = MagicMock()
mock_seesaw_instance = MagicMock()
mock_seesaw_instance.pin_mode = MagicMock()
mock_seesaw_instance.set_GPIO_interrupts = MagicMock()
mock_seesaw_instance.get_GPIO_interrupt_flag = MagicMock(return_value=0)
mock_seesaw_instance.digital_read_bulk = MagicMock(return_value=0xf0)
mock_seesaw.return_value = mock_seesaw_instance
sys.modules['adafruit_seesaw'] = MagicMock()
sys.modules['adafruit_seesaw.seesaw'] = MagicMock()
sys.modules['adafruit_seesaw.seesaw'].Seesaw = mock_seesaw

# Mock adafruit_seesaw.neopixel
# Create a list-like mock that supports indexing and len()
class MockNeoPixel:
    def __init__(self, *args, **kwargs):
        self._pixels = [0] * 4
    
    def __len__(self):
        return len(self._pixels)
    
    def __getitem__(self, index):
        return self._pixels[index]
    
    def __setitem__(self, index, value):
        self._pixels[index] = value

mock_neopixel = MagicMock()
mock_neopixel.NeoPixel = MockNeoPixel
mock_neopixel.GRB = "GRB"
sys.modules['adafruit_seesaw.neopixel'] = mock_neopixel

