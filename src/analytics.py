import datetime
import os
import json
from dataclasses import dataclass
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
from src.logger_config import log_app

load_dotenv()
PASSWORD = os.getenv("PASSWORD")
USERNAME = os.getenv("USERNAME")
DEP_DEPENDENCY = os.getcwd() + '\\data\\'
log_main = log_app('analytics')
day = datetime.datetime.now().strftime("%Y-%m-%d")
cluster = MongoClient(
    f'mongodb+srv://{USERNAME}:{PASSWORD}@mildata.oyy7jmp.mongodb.net/?retryWrites=true&w=majority')
db = cluster["milData"]
collection = db["historicalData"]
pd.options.mode.chained_assignment = None  # type: ignore


def load_pd_data(date=day):
    with open(DEP_DEPENDENCY + f'final_adsb{date}_main.json', 'r', encoding='UTF-8') as data_file:
        ac_df = json.load(data_file)
        data = pd.DataFrame(ac_df['mil_data'])
        log_main.info("Data loaded from 'final_adsb%s.json'", date)
        ac_data_frame = data.drop_duplicates('hex')
        ac_data_frame.drop(
            ac_data_frame[ac_data_frame['r'] == 'TWR'].index, inplace=True)
        ac_data_frame.drop(
            ac_data_frame[ac_data_frame['t'] == 'GND'].index, inplace=True)
        ac_data_frame.drop(
            ac_data_frame[ac_data_frame['flight'] == 'TEST1234'].index, inplace=True)
        ac_data_frame.fillna('No data available', inplace=True)
        log_main.info("Data written to 'final_adsb%s.json'", date)
    return ac_data_frame


def insert_data():
    with open(DEP_DEPENDENCY + f'final_adsb{day}_main.json', 'r', encoding='UTF-8') as mdb_i_file:
        data = json.load(mdb_i_file)
    with open(DEP_DEPENDENCY + f'final_adsb{day}_stats.json', 'r', encoding='UTF-8') as mdb_o_file:
        stats = json.load(mdb_o_file)
    with open(DEP_DEPENDENCY + f'final_adsb{day}_inter.json', 'w', encoding='UTF-8') as mdb_int_file:
        inter = json.load(mdb_int_file)
    collection.insert_many(
        {"_id": f"{day}", "data": data, "stats": stats, "inter": inter})


def get_mdb_data(date, specifed_file):
    if not os.path.exists(DEP_DEPENDENCY):
        os.makedirs(DEP_DEPENDENCY)
    results = collection.find_one({"_id": f"{date}"})
    with open(DEP_DEPENDENCY + f'final_adsb{date}_{specifed_file}.json', 'w', encoding='UTF-8') as mdb_file:
        try:
            if results is None:
                log_main.critical("Data for %s not found in database", date)
                return
            json.dump(results[f'{specifed_file}'], mdb_file, indent=2)
        except TypeError:
            log_main.critical(
                'Invalid date format. Please use YYYY-MM-DD format.')
            return


@dataclass
class Analytics:
    date: str = day

    ac_type = pd.Series(['EUFI', 'F16', 'V22', 'F18S', 'A10',
                        'F35LTNG', 'S61', 'H64', 'F15', 'AV8B', 'RC135'])
    callsign = pd.Series(['AF1', 'AF2'])
    er_flags = pd.Series(['7700', '7600', 'general', 'lifeguard',
                         'minfuel', 'nordo', 'unlawful', 'downed', 'reserved'])

    @classmethod
    def for_data(cls, date, info_req):
        """Date will be in YYYY-MM-DD format, provided by the UI"""
        t_data_frame = load_pd_data(date)

        try:
            log_main.info("%s data for %s fowarded to UI", info_req, cls.date)
            return pd.value_counts(t_data_frame[info_req]).to_dict()
        except KeyError:
            pass

    @classmethod
    def inter_ac(cls, date, row='t', data='ac_type'):
        """Used for special aircraft based on logic below"""

        t_data_frame = load_pd_data(date)

        try:
            if data == 'ac_type':
                interesting_data = cls.ac_type
            elif data == 'callsign':
                interesting_data = cls.callsign
            elif data == 'er_flags':
                interesting_data = cls.er_flags
            else:
                return 'Invalid data'

            d_file = t_data_frame[t_data_frame[row].isin(
                interesting_data)].to_dict(orient='records')
            log_main.info("Data written to 'final_adsb%s_inter.json'", date)
            return d_file
        except KeyError:
            log_main.critical(
                'Invalid data type. Please use ac_type, callsign or er_flags.')
            return
