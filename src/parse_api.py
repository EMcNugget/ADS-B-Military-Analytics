import datetime
import os
import json
from time import sleep
import time
import requests
from dotenv import load_dotenv
from src import analytics as an
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

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")
DEP_DEPENDENCY = os.getcwd() + '\\data\\'
log_main = log_app('api_processor')
day = datetime.date.today().strftime('%Y-%m-%d')

def dependencies():
    if not os.path.exists(DEP_DEPENDENCY):
        os.makedirs(DEP_DEPENDENCY)
    elif not os.path.exists(DEP_DEPENDENCY + 'adsb.json'):
        with open(DEP_DEPENDENCY + 'adsb.json', 'w', encoding='UTF-8') as data:
            data.write('')

def proccessed_data_setup():
    while True:
        if not os.path.exists(DEP_DEPENDENCY + f'final_adsb{day}.json'):
            with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'w', encoding='UTF-8') as file_data:
                file_data.write('{"mil_data":[\n')

def data_format():
    with open(DEP_DEPENDENCY + 'adsb.json', 'r', encoding='UTF-8') as file:
        data = file.read()
        database = json.loads(data)

    for aircraft in database['ac']:
        with open (DEP_DEPENDENCY + f'final_adsb{day}.json', 'a', encoding='UTF-8') as file:
            mil_data = json.dumps(aircraft, separators=(',', ': '))
            mil_data += ",\n"
            file.write(mil_data)

# API requests and proccessing

def get_data():
    """Gets data from the API and returns it as a string
    due to the API already formatting it to JSON"""

    url = "https://adsbexchange-com1.p.rapidapi.com/v2/mil/"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    try:
        response = requests.request("GET", url, headers=headers, timeout=3)
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
        sleep(DELAY)


def man_req():
    """Ability to manually request data from the API and write it to a JSON file"""

    while True:
        user = input("Enter 'req' to request")
        if user == "req":
            data = get_data()
            with open(DEP_DEPENDENCY + 'adsb.json', 'w', encoding='UTF-8') as file:
                file.write(str(data))
                log_main.info("Data written locally")
                data_format()
        else:
            print("Invalid input")
            log_main.warning("Invalid input")
def rollover():
    """Rollover function, runs every 24 hours"""

    while True:
        if time.strftime("%H:%M:%S", time.localtime()) == "23:59:15":
            with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'a', encoding='UTF-8') as rollover_file:
                try:
                    rollover_file.write('{"end": "end"}\n]}')
                    log_main.info("Data written to database")
                    log_main.info("File 'final_adsb%s.json' removed", day)
                except FileNotFoundError:
                    log_main.critical("File 'final_adsb%s.json' not found", day)
            
            with open(DEP_DEPENDENCY + f'final_adsb{day}_stats.json', 'w', encoding='UTF-8') as roll_data:
                try:
                    roll_data.write('{"data":[\n')
                    json_data = an.Analytics.for_data(day, 't')
                    json.dump(json_data, roll_data, indent=2)
                    roll_data.write('{"end": "end"}\n]}')
                except FileNotFoundError:
                    log_main.critical("File 'final_adsb%s_stats.json' not found", day)

            with open(DEP_DEPENDENCY + f'final_adsb{day}_inter.json', 'a', encoding='UTF-8') as inter_data:
                roll_data.write('{"end": "end"}\n]}')
                try:
                    inter_data.write('{"data":[\n')
                    json_stats = an.Analytics.inter_ac(day, 't')
                    json.dump(json_stats, inter_data, indent=2)
                    inter_data.write('{"end": "end"}\n]}')
                except FileNotFoundError:
                    log_main.critical("File 'final_adsb%s_inter.json' not found", day)
            an.insert_data()
            try:
                os.remove(DEP_DEPENDENCY + f'final_adsb{day}.json')
                os.remove(DEP_DEPENDENCY + f'final_adsb{day}_stats.json')
                os.remove(DEP_DEPENDENCY + f'final_adsb{day}_inter.json')
            except PermissionError:
                log_main.critical("File 'final_adsb%s.json' is currently in use", day)
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
    sleep(3)
    log_main.debug('API fetch successful')
    return True
