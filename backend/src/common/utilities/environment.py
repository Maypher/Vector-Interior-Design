from os import environ
from urllib.parse import urlparse

dev_mode = environ.get("DEV_MODE") == "1"
