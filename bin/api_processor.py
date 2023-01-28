import time
import http.client
import datetime
import os
import json
from dotenv import load_dotenv
from bin.loggerConfig import log_app

current_time = datetime.datetime.now().time()


if datetime.time(4, 0) <= current_time <= datetime.time(19, 0):
    time_var = 350
elif datetime.time(19, 0) < current_time <= datetime.time(23, 59):
    time_var = 750
elif datetime.time(0, 1) < current_time <= datetime.time(3, 59):
    time_var = 450
else:
    time_var = 550


load_dotenv()

LG_MAIN = log_app('api_processor')
API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")
DEP_DEPENDENCY = os.getcwd() + '\\data\\'
day = datetime.date.today().strftime('%d-%m-%Y')


conn = http.client.HTTPSConnection("adsbexchange-com1.p.rapidapi.com")

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}


# file system setup and formatting. The reason these 3 functions are in this file verus data_processor.py is because they are directly integrated with the API calling functions-
# It would be slower to import those functions here. 


def dependencies():
    if not os.path.exists(DEP_DEPENDENCY):
        os.makedirs(DEP_DEPENDENCY)
    elif not os.path.exists(DEP_DEPENDENCY + 'adsb.json'):
        with open(DEP_DEPENDENCY + 'adsb.json', 'w') as data:
            data.write('')


def proccessed_data_setup():
    while True:
        if not os.path.exists(DEP_DEPENDENCY + f'final_adsb{day}.json'):
            with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'w') as file_data:
                file_data.write('{"mil_data":[\n')


def data_format():
    with open(DEP_DEPENDENCY + 'adsb.json', 'r') as file:
        data = file.read()
        DB = json.loads(data)
        
        
    for v in DB['ac']:
        with open (DEP_DEPENDENCY + f'final_adsb{day}.json', 'a') as f:
            mil_data = json.dumps(v, separators=(',', ': '))
            mil_data += ",\n"
            f.write(mil_data)


# API requests and proccessing


def get_data():
    try:
        conn.request("GET", "/v2/mil/", headers=headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")
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


def rollover():
    while True:
        if time.strftime("%H:%M:%S", time.localtime()) == "23:59:00":
            with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'a') as f:
                    f.write('{"end": "end"}\n]}')
            time.sleep(1)
        else:
            pass


def api_check():
    data = get_data()
    if API_KEY is None or API_HOST is None:
        LG_MAIN.error('Invalid API_KEY or API_HOST | Code 1')
        return False
    elif data == '{"message":"You are not subscribed to this API."}':
        LG_MAIN.error('Invalid API_KEY or API_HOST | Code 2')
        return False
    elif not os.path.exists(".env"):
        LG_MAIN.error('No .env file found')
        return False
    else:
        time.sleep(3)
        LG_MAIN.debug('API fetch successful')
        return True
