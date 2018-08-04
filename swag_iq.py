import asyncio
import logging
import os
import time
from datetime import datetime
import json
import networking
import sys
import requests
import ssl

sys.dont_write_bytecode = True

# Read in bearer token and user ID
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "conn_settings.txt"), "r") as conn_settings:
    settings = conn_settings.read().splitlines()
    settings = [line for line in settings if line != "" and line != " "]

    try:
        BEARER_TOKEN_SWAG = settings[2].split("=")[1]
        # BEARER_TOKEN_VERIFICATION_SWAG = settings[3].split("=")[1]
        # BEARER_TOKEN_US = settings[0].split("=")[1]
    except IndexError as e:
        raise e

print("Getting...")
# verification_url = f"https://api.playswagiq.com/session/verify"
# verification_headers = {"authorization": f"Bearer {BEARER_TOKEN_VERIFICATION_SWAG}",
#                         "user-agent": "SwagIQ-Android/22 (okhttp/3.10.0)",
#                         "content-type": "application/x-www-form-urlencoded"}

main_url = f"https://api.playswagiq.com/trivia/home"
headers = {"Authorization": f"Bearer {BEARER_TOKEN_SWAG}",
           "User-Agent": "SwagIQ-Android/22",
           "Content-Type": "application/x-www-form-urlencoded"}

response_data = asyncio.get_event_loop().run_until_complete(networking.get_json_response_post(main_url, timeout=1.5, headers=headers))

print(response_data)
