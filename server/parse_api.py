"""Parses and checks ADSBExchange API, first round of pre-processing, and database insertion"""
import datetime
import os
import json
import time
import re
import requests
from . import analytics as an
from .logger_config import log_app

current_time = datetime.datetime.now().time()

if datetime.time(4, 0) <= current_time <= datetime.time(19, 0):
    DELAY = 350
elif datetime.time(19, 0) < current_time <= datetime.time(23, 59):
    DELAY = 750
elif datetime.time(0, 1) < current_time <= datetime.time(3, 59):
    DELAY = 450
else:
    DELAY = 550

API_KEY = os.environ["API_KEY"]
API_HOST = os.environ["API_HOST"]
DEP_DEPENDENCY = os.getcwd() + '\\data\\'
log_main = log_app('api_processor')
day = datetime.date.today().strftime('%Y-%m-%d')


def dependencies():
    """Creates the necessary directories and files for the program to run"""
    if not os.path.exists(DEP_DEPENDENCY):
        os.makedirs(DEP_DEPENDENCY)
    elif not os.path.exists(DEP_DEPENDENCY + 'adsb.json'):
        with open(DEP_DEPENDENCY + 'adsb.json', 'w', encoding='UTF-8') as data:
            data.write('')


def proccessed_data_setup():
    while True:
        if not os.path.exists(DEP_DEPENDENCY + f'final_adsb{day}_main.json'):
            with open(DEP_DEPENDENCY + f'final_adsb{day}_main.json', 'w', encoding='UTF-8') as file_data:
                file_data.write('[\n')


def data_format():
    with open(DEP_DEPENDENCY + 'adsb.json', 'r', encoding='UTF-8') as file:
        data = file.read()
        database = json.loads(data)
    with open(DEP_DEPENDENCY + f'final_adsb{day}_main.json', 'a', encoding='UTF-8') as file:
        json_array = database['ac']
        json_array_str = json.dumps(json_array, indent=2)
        data2 = re.sub(r'^\s*\[\s*|\s*\]\s*$', '',
                       json_array_str, flags=re.DOTALL)
        data3 = re.sub(r'}(?=\s*?({|$))', '},', data2)
        file.write(data3)
        file.write('\n')


def get_data():
    """Gets data from the API and returns it as a string
    due to the API already formatting it to JSON"""

    url = "https://adsbexchange-com1.p.rapidapi.com/v2/mil/"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    try:
        response = requests.request(
            "GET", url, headers=headers, timeout=3)  # type: ignore
        log_main.info("Data received from API")
        return response.text
    except TypeError as error:
        log_main.critical(error)


def auto_req():
    """Automatically requests data from the API and writes it to a JSON file
    at a specified interval as defined by the DELAY variable"""

    while True:
        data = get_data()
        with open(DEP_DEPENDENCY + 'adsb.json', 'w', encoding='UTF-8') as file:
            file.write(str(data))
            log_main.info("Data written locally")
            data_format()
        time.sleep(DELAY)


def interesting_data():
    with open(DEP_DEPENDENCY + f'final_adsb{day}_inter.json', 'w', encoding='UTF-8') as inter_data:
        try:
            json_stats = an.Analytics.inter_ac(day, 't', 'ac_type')
            if json_stats == []:
                json.dump({"hex": "No aircraft found"}, inter_data, indent=2)
            else:
                json.dump(json_stats, inter_data, indent=2)
        except FileNotFoundError:
            log_main.critical("File 'final_adsb%s_inter.json' not found", day)


def ac_count():
    with open(DEP_DEPENDENCY + f'final_adsb{day}_stats.json', 'w', encoding='UTF-8') as roll_data:
        try:
            json_data = an.Analytics.for_data(day, 't')
            json.dump(json_data, roll_data, indent=2)
        except FileNotFoundError:
            log_main.critical("File 'final_adsb%s_stats.json' not found", day)


def rollover():
    """Rollover function, runs every 24 hours"""

    while True:
        if time.strftime("%H:%M:%S", time.localtime()) == "23:59:45":
            with open(DEP_DEPENDENCY + f'final_adsb{day}_main.json', 'a+', encoding='UTF-8') as rollover_file:
                try:
                    rollover_file.seek(0, 2)
                    pos = rollover_file.tell()
                    while pos > 0:
                        pos -= 2
                        rollover_file.seek(pos)
                        if rollover_file.read(1) == "}":
                            break
                    rollover_file.truncate(pos)
                    rollover_file.write('}\n]')
                except FileNotFoundError:
                    log_main.critical(
                        "File 'final_adsb%s.json' not found", day)
            interesting_data()
            ac_count()
            an.insert_data()
            try:
                os.remove(DEP_DEPENDENCY + f'final_adsb{day}_main.json')
                os.remove(DEP_DEPENDENCY + f'final_adsb{day}_stats.json')
                os.remove(DEP_DEPENDENCY + f'final_adsb{day}_inter.json')
            except PermissionError:
                log_main.critical("File 'final_adsb%s.json' is open", day)
            log_main.info("Data written to database")
            time.sleep(1)


def api_check():
    """Checks the API key and host to ensure they are valid and that there is a .env file"""

    data = get_data()
    if API_KEY is None or API_HOST is None:
        log_main.error('Invalid API_KEY or API_HOST | Code 1')
        return False
    if data == '{"message":"You are not subscribed to this API."}':
        log_main.error('Invalid API_KEY or API_HOST | Code 2')
        return False
    if not os.path.exists(".env"):
        log_main.error('No .env file found')
        return False
    time.sleep(3)
    log_main.debug('API fetch successful')
    return True
