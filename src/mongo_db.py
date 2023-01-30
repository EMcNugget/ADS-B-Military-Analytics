from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
import datetime

load_dotenv()
MDB_URL = os.getenv("MONGO_DB_URL")
DEP_DEPENDENCY = os.getcwd() + '\\data\\'
day = datetime.datetime.now().strftime("%Y-%m-%d")
cluster = MongoClient(MDB_URL)
db = cluster["milData"]
collection = db["historicalData"]

def insert_data():
    with open(DEP_DEPENDENCY + f'final_adsb{day}.json', 'r') as file:
        data = json.load(file)
        collection.insert_one({"_id": f"{day}", "data": data})

def get_mdb_data(date):
    results = collection.find_one({"_id": f"{date}"})
    with open(DEP_DEPENDENCY + f'final_adsb{date}.json', 'w') as file:
        json.dump(results['data'], file, indent=2)
        