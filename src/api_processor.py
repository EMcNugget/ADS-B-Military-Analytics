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

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")
DEP_DEPENDENCY = os.getcwd() + '\\data\\'
log_main = log_app('api_processor')
day = datetime.date.today().strftime('%Y-%m-%d')

# file system setup and formatting. The reason these 3 functions are in this file
# verus data_processor.py is because they are directly integrated with the API calling functions
# It would be slower to import those functions here.

def dependencies():
    if not os.path.exists(DEP_DEPENDENCY):
        os.makedirs(DEP_DEPENDENCY)
    elif not os.path.exists(DEP_DEPENDENCY + 'adsb.json'):
        with open(DEP_DEPENDENCY + 'adsb.json', 'w', encoding='UTF-8') as data:
            data.write('')

def proccessed_data_setup():
    while True:
        if not os.path.exists(DEP_DEPENDENCY + f'final_adsb{day}.json'):
            with open(DEP_DEPENDENCY + 'final_adsb{day}.json', 'w', encoding='UTF-8') as file_data:
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
