""" Get the ball rolling """

import argparse
import signal
import sys
import logging
import time
import RPi.GPIO as GPIO
import board
from adafruit_seesaw.seesaw import Seesaw
from tunebox import display_controller, keypress_routines, handlers, owntone_wrapper, state_machine  # noqa:E501
from threading import Thread

INTERRUPT_GPIO = 6

logger = logging.getLogger('tunebox')
seesaw = Seesaw(board.I2C(), addr=0x30)


def main(argv):
    """ system setup and operation loop """

    # handle cli args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-ll',
        '--loglevel',
        default='info',
        help='Logging level. default=info'
    )
    args = parser.parse_args()

    # set logging loglevel
    logging.basicConfig(level=args.loglevel.upper())

    # setup GPIO mode
    GPIO.setmode(GPIO.BCM)

    # setup keyboard interrupt handling
    GPIO.setup(INTERRUPT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    for p in range(4, 8):
        seesaw.pin_mode(p, seesaw.INPUT_PULLUP)
    seesaw.set_GPIO_interrupts(240, True)
    print(seesaw.get_GPIO_interrupt_flag())
    GPIO.add_event_detect(INTERRUPT_GPIO,
                          GPIO.FALLING,
                          callback=handlers.keyboard_handler)

    # gather icons
    handlers.gather_icons()

    tbstate = state_machine.TuneboxState()

    # init keyboard
    key_set = {}
    for i in range(4):
        key_index = 240 ^ (1 << 4 + i)
        key_set[key_index] = handlers.Key(i + 1, keypress_routines.nothing)
    tbstate.keys = key_set

    # start forecast routine
    forecast_thread = Thread(target=handlers.weather_handler, args=(tbstate,))
    forecast_thread.daemon = True
    forecast_thread.start()

    # start owntone web socket connection
    owntone_wrapper.connect_socket()

    # let the state warm up
    time.sleep(5)

    # start the display controller
    display_controller.TuneboxDisplayController()

    # setup exit signal handler
    signal.signal(signal.SIGINT, handlers.signal_handler)
    signal.pause()


if __name__ == "__main__":
    main(sys.argv[1:])
