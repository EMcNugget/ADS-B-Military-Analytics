"""Main function contains functionality for the API and the UI, as well as the MongoDB queries and data processing"""

import os
import sys
import datetime
import time
import logging
from dataclasses import dataclass
from threading import Thread
import requests
import pandas as pd
from flask import jsonify
from dotenv import load_dotenv
from google.cloud import logging as gcloud_logging
from pymongo import MongoClient

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")
MDB_URL = os.getenv("MDB_URL")
cluster = MongoClient(MDB_URL)
db = cluster["milData"]
collection = db["historicalData"]

client = gcloud_logging.Client()
client.setup_logging()
logging.basicConfig(level=logging.info,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def current_time():
    """Returns time in UTC"""

    return datetime.datetime.now(datetime.timezone.utc).time()


def day():
    """Returns date as a datetime object"""

    return datetime.date.today()


def delay_time():
    """Sets the delay time based on the current time of day"""

    if datetime.time(4, 0) <= current_time() <= datetime.time(19, 0):
        return 350
    if datetime.time(19, 0) < current_time() <= datetime.time(23, 59):
        return 750
    if datetime.time(0, 1) < current_time() <= datetime.time(3, 59):
        return 450
    return 550


def get_data():
    """Gets data from the API and returns it as a JSON object"""

    url = "https://adsbexchange-com1.p.rapidapi.com/v2/mil/"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    response = requests.request(
        "GET", url, headers=headers, timeout=5)  # type: ignore
    data = response.json()
    if len(data) == 0:
        logging.warning("No data collected %s", current_time())
        return get_data()
    if response.status_code in [404, 400, 500]:
        logging.error("Error collecting data %s", current_time())
    logging.info("Data collected %s", current_time())
    return data


@dataclass
class Analysis:
    """Analysis of data"""

    final_data = {}
    dist_data = {}
    new_data = {}

    @classmethod
    def get_stats(cls, day_amount: int):
        """Returns a list of stats for the specified amount of days"""
        dist_data, final_data, new_data = cls.dist_data, cls.final_data, cls.new_data

        dist_data.clear()
        final_data.clear()
        new_data.clear()

        for i in range(day_amount):
            date = day() - datetime.timedelta(days=i)
            analysis = collection.find_one({"_id": date.strftime("%Y-%m-%d")})
            if analysis:
                dist_data.update({analysis['_id']: analysis['stats']})

        multi_index = [(date, row['type'])
                       for date, rows in dist_data.items() for row in rows]
        analysis_df = pd.DataFrame([row['value'] for rows in dist_data.values()
                                    for row in rows], index=pd.MultiIndex.from_tuples(multi_index))
        analysis_df = analysis_df.unstack(level=0)
        analysis_df.columns = analysis_df.columns.get_level_values(1)
        analysis_df.fillna(0, inplace=True)
        analysis_df.sort_values(
            by=analysis_df.columns[-1], axis=0, ascending=False, inplace=True)
        logging.info("Sorted data for %d at %s", day_amount, current_time())
        max_data = analysis_df.sum(axis=1).sort_values(ascending=False)
        max_data = max_data[:1].to_dict()
        final_data.update({"max": max_data})
        sum_dict = analysis_df.sum(axis=0).to_dict()
        sum_dict_int = {key: int(value) for key, value in sum_dict.items()}
        final_data.update({"sum": [{"type": t, "value": v}
                                   for t, v in sum_dict_int.items()]})
        mean_data = analysis_df.values.sum(axis=0)
        mean_data = sum(mean_data) / len(mean_data)
        final_data.update({"mean": int(mean_data)})
        logging.info("Calculated stats for %d at %s",
                     day_amount, current_time())
        return final_data


@dataclass
class Main:
    """Class for main, used to return data to the UI"""

    main_data = {}
    data = {}
    date: str = day().strftime("%Y-%m-%d")
    ac_type = pd.Series(['EUFI', 'F16', 'V22', 'F18S', 'A10',
                        'F35LTNG', 'F35', 'C2', 'E2', 'S61',
                         'B742', 'H64', 'F15',
                         'AV8B', 'RC135'])
    schema = {'hex': [], 'flight': [], 't': [],
              'r': [], 'squawk': [], 'lat': [], 'lon': []}

    @classmethod
    def pre_proccess(cls):
        """Removes duplicates and extraneous data"""

        for item in cls.main_data['ac']:
            if item['hex'] not in cls.schema['hex']:
                cls.schema['hex'].append(item['hex'])
                cls.schema['flight'].append(item.get('flight', 'None').strip())
                cls.schema['t'].append(item.get('t', 'None'))
                cls.schema['r'].append(item.get('r', 'None'))
                cls.schema['squawk'].append(item.get('squawk', 'None'))
                cls.schema['lat'].append(item.get('lat', 'None'))
                cls.schema['lon'].append(item.get('lon', 'None'))
        df_data = pd.DataFrame(cls.schema)
        df_data.drop(df_data[df_data['r'] == 'TWR'].index, inplace=True)
        df_data.drop(df_data[df_data['t'] == 'GND'].index, inplace=True)
        df_data.drop(df_data[df_data['flight'] =='TEST1234'].index, inplace=True) # fmt: off
        final_data = df_data.to_dict('records')
        logging.info("Data pre-proccessing complete %s", current_time())
        cls.data.update({"ac": final_data})

    @classmethod
    def auto_req(cls):
        """Automatically requests data from the API and writes it to a JSON file
        at a specified interval as defined by the DELAY variable"""

        while True:
            cls.main_data.update(get_data())
            cls.pre_proccess()
            time.sleep(delay_time())

    @staticmethod
    def get_days_in_month():
        """Returns the number of days in the current month"""

        month=datetime.datetime.now()

        if month.month in (1,3,5,7,8,10,12):
            return 31
        elif month.month in(4,6,9,11):
            return 30
        else:
            if month.year%4==0:
                return 29
            return 28


    @classmethod
    def mdb_insert(cls):
        """Inserts data into MongoDB"""

        doc = {"_id": datetime.date.today().strftime("%Y-%m-%d"),
               "data": cls.data['ac'],"stats": cls.ac_count(), 
               "inter": cls.inter_ac()}
        if datetime.datetime.today().strftime('%A') == 'Sunday':
            doc.update({"eow": Analysis.get_stats(7)})
            logging.info("Weekly analysis complete %s", current_time())
        else:
            pass
        if datetime.datetime.today().date() == 1:
            doc.update({"eom": Analysis.get_stats(cls.get_days_in_month())})
            logging.info("Monthly analysis complete %s", current_time())
        else:
            pass
        collection.insert_one(doc)

    @classmethod
    def ac_count(cls):
        """Returns the total number of aircraft in the data"""

        ac_data = pd.DataFrame(cls.pre_proccess())
        count = pd.value_counts(ac_data['t']).to_dict()
        new_list = []
        for key, value in count.items():
            new_dict = {"type": key, "value": value}
            new_list.append(new_dict)
        return new_list

    @classmethod
    def inter_ac(cls):
        """Returns objects that contain an aircraft type specified in the ac_type"""

        interesting_ac = pd.DataFrame(cls.data['ac'])
        inter_data = interesting_ac[interesting_ac['t'].isin(
            cls.ac_type)].to_dict(orient='records')
        if inter_data == []:
            return jsonify({"message": "No interesting aircraft found"})
        return inter_data


def rollover():
    """Checks the time every second and runs the mdb_insert function at 11:59:55pm"""

    while True:
        if datetime.datetime.now().strftime('%H:%M:%S') == '23:59:45':
            Main.mdb_insert()
            logging.info("Data inserted into MongoDB %s", current_time())
            Main.data.clear()
            Main.schema = {'hex': [], 'flight': [], 't': [], 'r': [], 'squawk': []}
            if Main.data:
                raise ValueError("Error Clearing Data")
            logging.info("Data cleared %s", current_time())
        time.sleep(1)

def api_func():
    """Main function for the project."""

    Thread(target=Main().auto_req).start()
    Thread(target=rollover).start()

if __name__ == '__main__':
    try:
        api_func()
        logging.info("Instance started %s", current_time())
    except KeyboardInterrupt as error:
        print(error)
        sys.exit(0)
