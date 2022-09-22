""" Get the ball rolling """

import argparse
import signal
import sys
import logging
import time
import RPi.GPIO as GPIO
from tunebox import display_controller, handlers, state_machine
from threading import Thread

INTERRUPT_GPIO = 6

logger = logging.getLogger('tunebox')


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
    GPIO.setup(INTERRUPT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(INTERRUPT_GPIO,
                          GPIO.FALLING,
                          callback=handlers.keyboard_handler)

    tbstate = state_machine.TuneboxState()

    # gather icons
    handlers.gather_icons()

    # start forecast routine
    forecast_thread = Thread(target=handlers.weather_handler, args=(tbstate,))
    forecast_thread.daemon = True
    forecast_thread.start()

    # let the state warm up
    time.sleep(10)

    # start the display controller
    display_controller.TuneboxDisplayController()

    # setup exit signal handler
    signal.signal(signal.SIGINT, handlers.signal_handler)
    signal.pause()


if __name__ == "__main__":
    main(sys.argv[1:])
