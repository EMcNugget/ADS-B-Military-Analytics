import os
import json
import datetime
from collections import defaultdict
import time
import pandas as pd
from src.mongo_db import insert_data
from src.logger_config import log_app

LG_MAIN = log_app('data_processor')
DEP_DEPENDENCY = os.getcwd() + '\\data\\'
day = datetime.date.today().strftime('%Y-%m-%d')

def remove_dup():
    with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'r') as file:
        try:
            data = json.load(file)
            LG_MAIN.info(f"Data loaded from 'final_adsb{day}.json'")
        except json.decoder.JSONDecodeError:
            LG_MAIN.critical(f"Error loading data from 'final_adsb{day}.json'")
        

    unique_flights = defaultdict(dict)


    for flight in data['mil_data']:
        unique_flights[flight.get("hex")] = flight


    with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'w') as data2:
        json.dump(unique_flights, data2, indent=2)


def remove_test1234():
    with open(DEP_DEPENDENCY + f'final_adsb{day}.json' , 'r') as file:
        data = json.load(file)


    for k, v in list(data.items()):
        try:
            if v['flight'] == 'TEST1234' or v['flight'] == 'GNDTEST ':
                del data[k]
        except KeyError:
            pass


    with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'w') as data2:
        json.dump(data, data2, indent=2)

def rollover():
    while True:
        if time.strftime("%H:%M:%S", time.localtime()) == "23:59:00":
            with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'a') as f:
                    f.write('{"end": "end"}\n]}')
                    try:
                        insert_data()
                        LG_MAIN.info("Data written to database")
                        os.remove(DEP_DEPENDENCY + f'final_adsb{day}.json')
                        LG_MAIN.info(f"File 'final_adsb{day}.json' removed")
                    except FileNotFoundError:
                        LG_MAIN.critical(f"File 'final_adsb{day}.json' not found")
            time.sleep(1)

def remove_dup_pd(): # WIP
    with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'r') as file:
        d = json.load(file)
        data = pd.DataFrame(d['mil_data'])
        LG_MAIN.info(f"Data loaded from 'final_adsb{day}.json'")
        fd = data.drop_duplicates(subset=['hex'], keep='first')
        fd.to_json(orient='records', indent=2) 

