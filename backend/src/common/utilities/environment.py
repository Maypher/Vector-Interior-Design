from os import environ

dev_mode = environ.get("BUILD_TARGET") == "dev"
