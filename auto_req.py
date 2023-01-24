import time
import requests
import datetime
import os
from threading import Thread
import logging
import logging.handlers
from dotenv import load_dotenv


class lg:
    def __init__(self):
        self.logger = logging.getLogger('auto_req')
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler = logging.handlers.RotatingFileHandler(
            f'adsb_main.log', maxBytes=1000000, backupCount=5)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)


current_time = datetime.datetime.now().time()

if datetime.time(4, 0) <= current_time <= datetime.time(19, 0):
    variable = 350
elif datetime.time(19, 0) < current_time <= datetime.time(23, 59):
    variable = 750
elif datetime.time(0, 1) < current_time <= datetime.time(3, 59):
    variable = 450
else:
    variable = 550

load_dotenv()

LG_MAIN = lg().logger
API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")
DEP_DEPENDENCY = os.path.join(os.path.dirname(__file__), 'data\\')


url = "https://adsbexchange-com1.p.rapidapi.com/v2/mil/"
headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}


def dependenies():
    if not os.path.exists(DEP_DEPENDENCY):
        os.makedirs(DEP_DEPENDENCY)
    elif not os.path.exists(DEP_DEPENDENCY + 'adsb.json'):
        with open(DEP_DEPENDENCY + 'adsb.json', 'w') as data:
            data.write('[]')


def get_data():
    try:
        response = requests.request("GET", url, headers=headers)
        return response.text
    except Exception as e:
        LG_MAIN.error(e)


def check_api():
    data = get_data()
    if API_KEY is None or API_HOST is None:
        LG_MAIN.error(
            "API_KEY or API_HOST is not set or is invalid")
        print("API_KEY or API_HOST is not set or is invalid")
        exit()
    elif data == '"message":"You are not subscribed to this API."':
        LG_MAIN.error(
            "API_KEY is invalid")
        exit()
    else:
        LG_MAIN.info("API_KEY and API_HOST are valid")
        return True


def auto_req():
    while True:
        try:
            data = get_data()
            with open(DEP_DEPENDENCY + 'adsb.json', 'a') as file:
                file.write(str(data))
                LG_MAIN.info("Data written to database automatically")
            time.sleep(variable)
        except Exception as e:
            LG_MAIN.error(e)
        time.sleep(variable)


def man_req():
    while True:
        user = input("Enter 'req' to request")
        try:
            if user == "req":
                data = get_data()
                with open(DEP_DEPENDENCY + 'adsb.json', 'a') as file:
                    file.write(str(data))
                    LG_MAIN.info("Data written to database manually")
            else:
                print("Invalid input")
                LG_MAIN.warning("Invalid input")
        except Exception as e:
            LG_MAIN.error(e)


if __name__ == "__main__":
    check_api()
    while True:
        dependenies()
        Thread(target=auto_req).start()
        Thread(target=man_req).start()
