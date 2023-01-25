import time
import requests
import datetime
import os
from threading import Thread
import logging
import logging.handlers
import json
from dotenv import load_dotenv


load_dotenv()
current_time = datetime.datetime.now().time()

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('auto_req')
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler = logging.handlers.RotatingFileHandler(
            'adsb_main.log', maxBytes=1000000, mode='w', backupCount=5)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)


if datetime.time(4, 0) <= current_time <= datetime.time(19, 0):
    time_var = 350
elif datetime.time(19, 0) < current_time <= datetime.time(23, 59):
    time_var = 750
elif datetime.time(0, 1) < current_time <= datetime.time(3, 59):
    time_var = 450
else:
    time_var = 550


LG_MAIN = Logger().logger
API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")
DEP_DEPENDENCY = os.path.join(os.path.dirname(__file__), 'data\\')


url = "https://adsbexchange-com1.p.rapidapi.com/v2/mil/"
headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

# file system setup and formatting

def dependencies():
    if not os.path.exists(DEP_DEPENDENCY):
        os.makedirs(DEP_DEPENDENCY)
    elif not os.path.exists(DEP_DEPENDENCY + 'adsb.json'):
        with open(DEP_DEPENDENCY + 'adsb.json', 'w') as data:
            data.write('')


def proccessed_data_setup():
    if not os.path.exists(DEP_DEPENDENCY + 'final_adsb.json'):
        with open(DEP_DEPENDENCY + 'final_adsb.json', 'w') as file_data:
            file_data.write('{"mil_data":[\n')


def data_format():
    with open(DEP_DEPENDENCY + 'adsb.json', 'r') as file:
        data = file.read()
        DB = json.loads(data)
        
        
    for v in DB['ac']:
        with open (DEP_DEPENDENCY + 'final_adsb.json', 'a') as f:
            mil_data = json.dumps(v, separators=(',', ': '))
            mil_data += ",\n"
            f.write(mil_data)

# API requests and proccessing

def get_data():
    try:
        response = requests.request("GET", url, headers=headers)
        return response.text
    except Exception as e:
        LG_MAIN.error(e)


def auto_req():
    while True:
        try:
            data = get_data()
            with open(DEP_DEPENDENCY + 'adsb.json', 'w') as file:
                file.write(str(data))
                LG_MAIN.info("Data written to database automatically")     
                data_format()            
            time.sleep(time_var)
        except Exception as e:
            LG_MAIN.error(e)
        time.sleep(time_var)


def man_req():
    while True:
        user = input("Enter 'req' to request")
        try:
            if user == "req":
                data = get_data()
                with open(DEP_DEPENDENCY + 'adsb.json', 'w') as file:
                    file.write(str(data))
                    LG_MAIN.info("Data written to database manually")
                    data_format()
            else:
                print("Invalid input")
                LG_MAIN.warning("Invalid input")
        except Exception as e:
            LG_MAIN.error(e)


def api_check():
    data = get_data()
    if API_HOST or API_KEY is None:
        LG_MAIN.error('Invalid API_KEY or API_HOST')
        return False
    elif data == '{"message":"You are not subscribed to this API."}':
        LG_MAIN.error('Invalid API_KEY or API_HOST')
        return False
    else:
        time.sleep(3)
        LG_MAIN.debug('API fetch successful')
        return True
    

def main():
    if api_check():
        dependencies()
        proccessed_data_setup()
        Thread(target=auto_req).start()
        Thread(target=man_req).start()
    else:
        exit()

if __name__ == "__main__":
    main()

# --TODO--

# -Remove duplicates from "final_adsb.json"

# -Remove all dictionaries containing the callsign "TEST1234"

# -Automatically add "]}" to the end of "final_adsb.json"

# -Send proccessed data to MongoDB


# --Future--


# -Create front end with CustomTkinter or PyPQt6

# -Web version?