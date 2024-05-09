import os
try:
    import requests
    import time
    import colored
    import datetime
except ModuleNotFoundError:
    os.system('pip install colored')
    os.system('pip install datetime')
    os.system('pip install requests')
from time import sleep
from colored import fg, attr, bg

gray = fg("dark_gray")
reset = attr("reset")
purple = fg("purple_1a")

TOKEN = "your token"
STATUS = "dnd"  # online, idle, invisible, dnd
STATUS_TEXT = ['1', '2', '3'] # you can add more text

current_status_index = 0

def info(message, with_loading=False):
    current_time = datetime.datetime.now().strftime(f"{gray}%H:%M:%S{reset}")
    if with_loading:
        print(f"{current_time} {purple}INF {gray}>{reset} {message}", end='', flush=True)
        for _ in range(3):
            sleep(0.2)
            print(".", end='', flush=True)
        print()
    else:
        print(f"{current_time} {purple}INF {gray}>{reset} {message}")

while True:
    header ={
        'authorization': TOKEN
    }

    choosedStatus = STATUS_TEXT[current_status_index]

    jsonData = {
        "status": STATUS, 
        "custom_status": {
            "text": choosedStatus,
        } 
    }
    try:
        r = requests.patch("https://discord.com/api/v8/users/@me/settings", headers=header, json=jsonData)
        if r.status_code == 200:
            info(f"Status successfully changed by '{choosedStatus}' -> {r.status_code} {bg('purple_1a')} {fg('white')}OK {attr('reset')}")
        elif r.status_code == 429:
            data = r.json()
            retry_after = data['retry_after']
            info("Ratelimited {}".format(retry_after))
            sleep(int(retry_after))
        else:
            info("Failed to change status -> {}".format(r.status_code))
        
        current_status_index = (current_status_index + 1) % len(STATUS_TEXT)

    except TimeoutError as e:
        info(e)

    sleep(5) # time to change status edit it if you need
