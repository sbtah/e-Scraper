import os
from dotenv import load_dotenv


load_dotenv()


MAIN_URL = os.environ.get("MAIN_URL")
STORES_URL = os.environ.get("STORES_URL")

