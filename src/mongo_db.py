import datetime
import os
import json
from dataclasses import dataclass, field
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
from .logger_config import log_app

load_dotenv()
MDB_URL = os.getenv("MONGO_DB_URL")
DEP_DEPENDENCY = os.getcwd() + '\\data\\'
log_main = log_app('mongo_db')
day = datetime.datetime.now().strftime("%Y-%m-%d")
cluster = MongoClient(MDB_URL)
db = cluster["milData"]
collection = db["historicalData"]

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
    ac_type: list = field(default_factory= lambda: ['EUFI', 'F16', 'V22', 'F18S', 'A10', 'F35LTNG', 'S61', 'H64', 'F15'])
    callsign: list = field(default_factory= lambda: ['AF1', 'AF2'])
    
    with open(DEP_DEPENDENCY + 'final_adsb2023-01-31.json', 'r', encoding='UTF-8') as file:
        ac_data = json.load(file)
        t_data_frame = pd.DataFrame(ac_data)
        t_data_frame.fillna('No type available', inplace=True)

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
        with open (DEP_DEPENDENCY + 'final_adsb2023-01-312.json', 'w', encoding='UTF-8') as file:
            try:
                json.dump(cls.t_data_frame[cls.t_data_frame['t'].isin(cls.ac_type)].to_dict(orient='records'), file, indent=2)
            except KeyError as error:
                log_main.critical(error)
                return
 
