import time
from random import randint

from scraper.helpers.logging import logging


def random_sleep_small():
    """Custom sleep function that sleeps from 3 to 6 seconds"""

    value = randint(1, 3)
    logging.info(f"Random small sleep call {value}")
    return time.sleep(value)


def random_sleep_small_l2():
    """Custom sleep function that sleeps from 3 to 6 seconds"""

    value = randint(3, 6)
    logging.info(f"Random small (2) sleep call {value}")
    return time.sleep(value)


def random_sleep_medium():
    """Custom sleep function that sleeps from 3 to 6 seconds"""

    value = randint(6, 8)
    logging.info(f"Random medium sleep call {value}")
    return time.sleep(value)


def random_sleep_large():
    """Custom sleep function that sleeps from 3 to 6 seconds"""

    value = randint(15, 20)
    logging.info(f"Random large sleep call {value}")
    return time.sleep(value)
