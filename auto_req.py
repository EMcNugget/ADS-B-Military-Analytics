import time
import requests
import datetime
import os
from threading import Thread
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")
DEP_DEPENDENCY = os.path.join(os.path.dirname(__file__), 'data\\')

current_time = datetime.datetime.now().time()

if datetime.time(4, 0) <= current_time <= datetime.time(19, 0):
    variable = 350
elif datetime.time(19, 0) < current_time <= datetime.time(23, 59):
    variable = 750
elif datetime.time(0, 1) < current_time <= datetime.time(3, 59):
    variable = 450
else:
    variable = 550

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
    response = requests.request("GET", url, headers=headers)
    return response.text


def auto_req():
    while True:
        try:
            data = get_data()
            with open(DEP_DEPENDENCY + 'adsb.json', 'a') as file:
                file.write(str(data))
            time.sleep(variable)
        except Exception as e:
            logger.error(e)
        time.sleep(variable)

def man_req():
    user = input("Enter 'req' to request")
    try:
        if user == "req":
            data = get_data()
            with open(DEP_DEPENDENCY + 'adsb.json', 'a') as file:
                file.write(str(data))
        else:
            print("Invalid input")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    dependenies()
    Thread(target=auto_req).start()
    Thread(target=man_req).start()


