import datetime
import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
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
                log_main.critical(f"Data for {date} not found in database")
                return
            json.dump(results['data'], file, indent=2)
        except TypeError:
            log_main.critical('Invalid date format. Please use YYYY-MM-DD format.')
