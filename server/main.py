"""Main function contains functionality for the API and the UI, as well as the MongoDB queries and data processing"""

import os
import sys
import datetime
import time
import logging
from dataclasses import dataclass, field
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
logging.basicConfig(level=logging.DEBUG,
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

    data: list = field(default_factory=list)
    final_data: dict = field(default_factory=dict)
    dist_data: dict = field(default_factory=dict)
    new_data: dict = field(default_factory=dict)

    # All type ignore are due to false positives from Pandas and don't affect functionality

    @staticmethod
    def get_stats(day_amount: int):
        """Returns a list of stats for the specified amount of days"""
        analysis_class = Analysis()
        dist_data = analysis_class.dist_data
        data = analysis_class.data
        final_data = analysis_class.final_data
        new_data = analysis_class.new_data

        for i in range(day_amount):
            date = day() - datetime.timedelta(days=i)
            data.append(date.strftime("%Y-%m-%d"))

        for date in data:
            analysis = collection.find_one({"_id": date})
            if analysis is None:
                pass
            else:
                dist_data.update({analysis['_id']: analysis['stats']})

        multi_index = [(date, row['type'])
                       for date, rows in dist_data.items() for row in rows]
        analysis_df = pd.DataFrame([row['value'] for rows in dist_data.values()
                                    for row in rows], index=pd.MultiIndex.from_tuples(multi_index))
        analysis_df = analysis_df.unstack(level=0)
        analysis_df.columns = analysis_df.columns.get_level_values(1)
        analysis_df.fillna(0, inplace=True)
        analysis_df.sort_values(
            by=analysis_df.columns[-1], axis=0, ascending=False, inplace=True)  # type: ignore
        logging.info("Sorted data for %d at %s", day_amount, current_time())
        max_data = analysis_df.sum(axis=1).sort_values(  # type: ignore
            ascending=False)
        final_data.update(
            {"max": {"type": max_data.index[0], "value": int(max_data[0])}})
        sum_dict = analysis_df.sum(axis=0).to_dict()
        sum_dict_int = {key: int(value) for key, value in sum_dict.items()}
        final_data.update({"sum": sum_dict_int})
        mean_data = analysis_df.values.sum(axis=0)  # type: ignore
        mean_data = sum(mean_data) / len(mean_data)
        final_data.update({"mean": int(mean_data)})
        logging.info("Calculated stats for %d at %s",
                     day_amount, current_time())
        for key, value in final_data.items():
            if key == "sum":
                new_data[key] = [{"type": t, "value": v}
                                 for t, v in value.items()]
            else:
                new_data[key] = {"type": None, "value": value} if isinstance(
                    value, int) else value
        logging.info("Formatted data for %d at %s", day_amount, current_time())
        return new_data


@dataclass
class Main:
    """Class for main, used to return data to the UI"""

    main_data: dict = field(default_factory=dict)
    date: str = day().strftime("%Y-%m-%d")
    ac_type = pd.Series(['EUFI', 'F16', 'V22', 'F18S', 'A10',
                        'F35LTNG', 'F35', 'C2', 'E2', 'S61',
                         'B742\nBoeing E-4B', 'H64', 'F15',
                         'AV8B', 'RC135'])
    schema = {'hex': [], 'flight': [], 't': [], 'r': [], 'squawk': []}

    @classmethod
    def pre_proccess(cls):
        """Removes duplicates and extraneous data"""
        main = Main()
        main_data = main.main_data

        for item in main_data['ac']:
            hex_val = item['hex']
            if hex_val not in cls.schema['hex']:
                cls.schema['hex'].append(hex_val)
                cls.schema['flight'].append(item.get('flight', 'None').strip())
                cls.schema['t'].append(item.get('t', 'None'))
                cls.schema['r'].append(item.get('r', 'None'))
                cls.schema['squawk'].append(item.get('squawk', 'None'))
        df_data = pd.DataFrame(cls.schema)
        df_data.drop(df_data[df_data['r'] == 'TWR'].index, inplace=True)
        df_data.drop(df_data[df_data['t'] == 'GND'].index, inplace=True)
        df_data.drop(df_data[df_data['flight'] =='TEST1234'].index, inplace=True) # fmt: off
        final_data = df_data.to_dict('records')
        logging.debug("Data pre-proccessing complete %s", current_time())
        return final_data

    @classmethod
    def auto_req(cls):
        """Automatically requests data from the API and writes it to a JSON file
        at a specified interval as defined by the DELAY variable"""

        main = Main()
        main_data = main.main_data

        while True:
            main_data.update(get_data())
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
               "data": cls.pre_proccess(),"stats": cls.ac_count(), 
               "inter": cls.inter_ac()}
        if datetime.datetime.today().strftime('%A') == 'Sunday':
            doc.update({"eow": Analysis.get_stats(7)})
            logging.debug("Weekly analysis complete %s", current_time())
        else:
            pass
        if datetime.datetime.today().date() == 1:
            doc.update({"eom": Analysis.get_stats(cls.get_days_in_month())})
            logging.debug("Monthly analysis complete %s", current_time())
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

        interesting_ac = pd.DataFrame(cls.pre_proccess())
        inter_data = interesting_ac[interesting_ac['t'].isin(
            cls.ac_type)].to_dict(orient='records')
        if inter_data == []:
            return jsonify({"message": "No interesting aircraft found"})
        return inter_data


def rollover():
    """Checks the time every second and runs the mdb_insert function at 11:59:55pm"""

    while True:
        if datetime.datetime.now().strftime('%H:%M:%S') == '23:59:50':
            Main.mdb_insert()
            logging.info("Data inserted into MongoDB %s", current_time())
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
