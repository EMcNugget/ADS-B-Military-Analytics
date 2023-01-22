import time
import requests
import logging
import datetime
import os
import cred

current_time = datetime.datetime.now().time()

# Due to likely uptick in mil traffic, data is requested more frequently to catch more rare aircraft.
if datetime.time(4, 0) <= current_time <= datetime.time(19, 0):
    variable = 350
# Due to it being night in the UK and US traffic is winding down data is requested less frequently to save API requests.
elif datetime.time(19, 0) < current_time <= datetime.time(23, 59):
    variable = 750
# Transition period for mil aircraft activity in the UK.
elif datetime.time(0, 1) < current_time <= datetime.time(3, 59):
    variable = 450
else:
    # Intermediate to catch other traffic during the downtimes of both US and UK traffic.
    variable = 550

log_directory = "data\\"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(level=logging.INFO, filename=os.path.join(
    log_directory, "adsb.json"), filemode='a')

url = "https://adsbexchange-com1.p.rapidapi.com/v2/mil/"
headers = {
    "X-RapidAPI-Key": cred.API_KEY,
    "X-RapidAPI-Host": cred.API_HOST
}


def get_data():
    response = requests.request("GET", url, headers=headers)
    logging.info(response.text)


while True:
    try:
        get_data()
        print(f"Data requested at {datetime.datetime.now()}")
    except Exception as e:
        print(e)
        logging.error(e)
    time.sleep(variable)
