import datetime
import os
import json
from dataclasses import dataclass
import time
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
from .logger_config import log_app

load_dotenv()
MDB_URL = os.getenv("MONGO_DB_URL")
DEP_DEPENDENCY = os.getcwd() + '\\data\\'
log_main = log_app('analytics')
day = datetime.datetime.now().strftime("%Y-%m-%d")
cluster = MongoClient(MDB_URL)
db = cluster["milData"]
collection = db["historicalData"]
pd.options.mode.chained_assignment = None

def rollover():
    """Rollover function, runs every 24 hours"""

    while True:
        if time.strftime("%H:%M:%S", time.localtime()) == "23:59:00":
            with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'a', encoding='UTF-8') as file:
                file.write('{"end": "end"}\n]}')
                try:
                    # insert_data()  # Keep this as commented out while testing items
                    log_main.info("Data written to database")
                    os.remove(DEP_DEPENDENCY + f'final_adsb{day}.json')
                    log_main.info("File 'final_adsb%s.json' removed", day)
                except FileNotFoundError:
                    log_main.critical("File 'final_adsb%s.json' not found", day)
            time.sleep(1)

def load_pd_data():
    with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'r', encoding='UTF-8') as file:
        ac_df = json.load(file)
        data = pd.DataFrame(ac_df['mil_data'])
        log_main.info("Data loaded from 'final_adsb%s.json'", day)
        ac_data_frame = data.drop_duplicates('hex')
        ac_data_frame.drop(ac_data_frame[ac_data_frame['r'] == 'TWR'].index, inplace=True)
        ac_data_frame.drop(ac_data_frame[ac_data_frame['t'] == 'GND'].index, inplace=True)
        ac_data_frame.drop(ac_data_frame[ac_data_frame['flight'] == 'TEST1234'].index, inplace=True)
        ac_data_frame.fillna('No data available', inplace=True)
        ac_data_frame.to_json(DEP_DEPENDENCY + f'final_adsb{day}.json', orient='records', indent=2)
        log_main.info("Data written to 'final_adsb%s.json'", day)

def insert_data():
    with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)
        collection.insert_one({"_id": f"{day}", "data": data})

def get_mdb_data(date):
    if not os.path.exists(DEP_DEPENDENCY):
        os.makedirs(DEP_DEPENDENCY)
    results = collection.find_one({"_id": f"{date}"})
    with open(DEP_DEPENDENCY + f'final_adsb{date}.json', 'w', encoding='UTF-8') as file:
        try:
            if results is None:
                log_main.critical("Data for %s not found in database", date)
                return
            json.dump(results['data'], file, indent=2)
        except TypeError:
            log_main.critical('Invalid date format. Please use YYYY-MM-DD format.')
            return
@dataclass
class Analytics:
    date: str = day

    ac_type = pd.Series(['EUFI', 'F16', 'V22', 'F18S', 'A10', 'F35LTNG', 'S61', 'H64', 'F15', 'AV8B', 'RC135'])
    callsign = pd.Series(['AF1', 'AF2'])

    with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'r', encoding='UTF-8') as file:
        ac_data = json.load(file)
        t_data_frame = pd.DataFrame(ac_data)

    @classmethod
    def for_data(cls, info_req):
        """Date will be in YYYY-MM-DD format, provided by the UI"""

        try:
            log_main.info("%s data for %s fowarded to UI", info_req, cls.date)
            return pd.value_counts(cls.t_data_frame[info_req]).to_dict()
        except KeyError:
            pass

    @classmethod
    def inter_ac(cls):
        """Used for most interesting aircraft based on logic below"""
        with open (DEP_DEPENDENCY + f'final_adsb{day}_stats.json', 'w', encoding='UTF-8') as file:
            try:
                json.dump(cls.t_data_frame[cls.t_data_frame['t'].isin(cls.ac_type)].to_dict(orient='records'), file, indent=2)
            except KeyError as error:
                log_main.critical(error)
                return
