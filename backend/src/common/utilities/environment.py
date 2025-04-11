from os import environ

dev_mode = environ.get("DEV_MODE") == "1"

# To allow for development in http and deployment in https this removes the protocol and port
# https is only added for CORS on app setup. Cookies don't require protocol or port thus it is removed
frontend_url = (
    environ.get("FRONTEND_URL")
    .removeprefix("http://")
    .removeprefix("https://")
    .split(":")[0]
)
