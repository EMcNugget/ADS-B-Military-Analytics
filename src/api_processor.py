import datetime # datetime is used to determine the time of day and set the delay time accordingly
import os # os is used to create the file system and check for the .env file
import json
from time import sleep # sleep is used to delay the API calls to prevent overloading the API
import requests
from dotenv import load_dotenv
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

log_main = log_app('api_processor')
API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")
DEP_DEPENDENCY = os.getcwd() + '\\data\\'
day = datetime.date.today().strftime('%Y-%m-%d')

# file system setup and formatting. The reason these 3 functions are in this file
# verus data_processor.py is because they are directly integrated with the API calling functions
# It would be slower to import those functions here.

def dependencies()-> None:
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
    url = "https://adsbexchange-com1.p.rapidapi.com/v2/mil/"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

# Type error for headers may occur
# if API_KEY or API_HOST are not set in .env, however this is dealt with in the API check function
    try:
        response = requests.request("GET", url, headers=headers, timeout=3)
        log_main.info("Data received from API")
        return response.text
    except TypeError as error:
        log_main.critical(error)


def auto_req():
    while True:
        try:
            data = get_data()
            with open(DEP_DEPENDENCY + 'adsb.json', 'w', encoding='UTF-8') as file:
                file.write(str(data))
                log_main.info("Data written locally")
                data_format()
            sleep(DELAY)
        except Exception as error:
            log_main.error(error)
        sleep(DELAY)

def man_req():
    while True:
        user = input("Enter 'req' to request")
        try:
            if user == "req":
                data = get_data()
                with open(DEP_DEPENDENCY + 'adsb.json', 'w', encoding='UTF-8') as file:
                    file.write(str(data))
                    log_main.info("Data written locally")
                    data_format()
            else:
                print("Invalid input")
                log_main.warning("Invalid input")
        except Exception as error:
            log_main.error(error)

def api_check():
    data = get_data()
    if API_KEY is None or API_HOST is None:
        log_main.error('Invalid API_KEY or API_HOST | Code 1')
        return False
    elif data == '{"message":"You are not subscribed to this API."}':
        log_main.error('Invalid API_KEY or API_HOST | Code 2')
        return False
    elif not os.path.exists(".env"):
        log_main.error('No .env file found')
        return False
    else:
        sleep(3)
        log_main.debug('API fetch successful')
        return True
