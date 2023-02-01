import os
import json
import datetime
from collections import defaultdict
import time
from .mongo_db import insert_data
from .logger_config import log_app

log_main = log_app('data_processor')
DEP_DEPENDENCY = os.getcwd() + '\\data\\'
day = datetime.date.today().strftime('%Y-%m-%d')

def remove_dup():
    unique_flights = defaultdict(dict)

    with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'r', encoding='UTF-8') as file:
        try:
            data = json.load(file)
            log_main.info(f"Data loaded from final_adsb{day}.json")
            for flight in data['mil_data']:
                unique_flights[flight.get("hex")] = flight
        except json.decoder.JSONDecodeError:
            log_main.critical(f"Error loading data from 'final_adsb{day}.json'")

    with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'w', encoding='UTF-8') as data2:
        json.dump(unique_flights, data2, indent=2)


def remove_test1234():
    with open(DEP_DEPENDENCY + f'final_adsb{day}.json' , 'r', encoding='UTF-8') as file:
        data = json.load(file)


    for key, sub_data in list(data.items()):
        try:
            if sub_data['flight'] == 'TEST1234' or sub_data['flight'] == 'GNDTEST ':
                del data[key]
        except KeyError:
            pass


    with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'w', encoding='UTF-8') as data2:
        json.dump(data, data2, indent=2)

def rollover():
    while True:
        if time.strftime("%H:%M:%S", time.localtime()) == "23:59:00":
            with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'a', encoding='UTF-8') as f:
                f.write('{"end": "end"}\n]}')
                try:
                    insert_data()
                    log_main.info("Data written to database")
                    os.remove(DEP_DEPENDENCY + f'final_adsb{day}.json')
                    log_main.info(f"File 'final_adsb{day}.json' removed")
                except FileNotFoundError:
                    log_main.critical(f"File 'final_adsb{day}.json' not found")
            time.sleep(1)
