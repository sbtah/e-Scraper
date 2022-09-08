import logging
import time
from random import randint
from urllib.parse import urljoin
import re


def random_sleep_small():
    """Custom sleep function that sleeps from 3 to 6 seconds"""

    value = randint(1, 3)
    logging.info(f"Random small sleep call {value}")
    return time.sleep(value)


def random_sleep_medium():
    """Custom sleep function that sleeps from 3 to 6 seconds"""

    value = randint(6, 8)
    logging.info(f"Random medium sleep call {value}")
    return time.sleep(value)


def my_float(string):
    """Sometimes we encounter a float value with ',' we need to change that to '.'"""

    if isinstance(string, str):
        try:
            str_to_use = string.replace(",", ".")
            return float(str_to_use)
        except Exception as e:
            logging.error(f"(my_float)Some other exeption : {e}")
            pass
    else:
        return float(string)


def clean_text(text):
    """Removes white space and new lines."""

    out_put_text = text.replace("\n", "")
    final_text = out_put_text.replace(" ", "")
    return final_text


def clean_stock_text_to_number(text):
    """Return only digits."""
    new_number = text.replace("(", "")
    return new_number


def extract_text_child_category_name(raw_text):
    match = re.search(r"(\n+\s+)(.*)(\n+\s+)", raw_text)
    extracted = match.group(2)
    return extracted
