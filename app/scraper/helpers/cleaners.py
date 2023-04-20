import re


def extract_price_data(data):
    """
    Sometimes, depending from Website price data can come in different formats.
    Regex help us here to extract only numeric values needed.
    """
    match = re.search(r"\d+[\,,\.]*\d+[\,,\.]*\d+", data)
    return str(match.group())
