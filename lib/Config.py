import os
from dotenv import load_dotenv
import datetime

load_dotenv('utf-8')

ROOT_URI = os.getenv("ROOT_URI")
BASE_DIR = os.getcwd()
AUTHENTICATION_URI = f"{ROOT_URI}/auth/userpass"
USERNAME = os.getenv("USERNAME", "your_username")
PASSWORD = repr(os.getenv("PASSWORD","your_password")).strip("'\"")
EARLIEST_DATE = os.getenv("EARLIEST_DATE")
ANALYST_LEVEL = os.getenv("ANALYST_LEVEL", "L1")

def get_current_timestamp():
    """Generates a fresh timestamp every time it is called."""
    return f"{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')}Z"