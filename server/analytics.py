"""All pre and post data proccessing"""
import datetime
import os
import json
from dataclasses import dataclass
from pymongo import MongoClient
import pandas as pd
from flask import Flask, jsonify, Response
from flask_cors import CORS
from .logger_config import log_app

MDB_URL = os.environ["MDB_URL"]
DEP_DEPENDENCY = os.getcwd() + '\\data\\'
log_main = log_app('analytics')
day = datetime.datetime.now().strftime("%Y-%m-%d")
cluster = MongoClient(MDB_URL)
db = cluster["milData"]
collection = db["historicalData"]
pd.options.mode.chained_assignment = None  # type: ignore

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
CORS(app)
app.config.from_mapping(config)

def load_pd_data(date: str=day):
    """Loads data from the JSON file and returns it as a pandas dataframe for further processing"""
    with open(DEP_DEPENDENCY + f'final_adsb{date}_main.json', 'r', encoding='UTF-8') as data_file:
        ac_df = json.load(data_file)
        data = pd.DataFrame(ac_df)
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
    """Inserts data into the database, and creates a cache file"""

    with open(DEP_DEPENDENCY + f'final_adsb{day}_main.json', 'r', encoding='UTF-8') as mdb_i_file:
        data = json.load(mdb_i_file)
    with open(DEP_DEPENDENCY + f'final_adsb{day}_stats.json', 'r', encoding='UTF-8') as mdb_o_file:
        stats = json.load(mdb_o_file)
    with open(DEP_DEPENDENCY + f'final_adsb{day}_inter.json', 'r', encoding='UTF-8') as mdb_int_file:
        inter = json.load(mdb_int_file)
    doc = {"_id": f"{day}", "data": data, "stats": stats, "inter": inter}
    collection.insert_one(doc)
    os.remove(DEP_DEPENDENCY + f'final_adsb{day}_main.json')
    os.remove(DEP_DEPENDENCY + f'final_adsb{day}_stats.json')
    os.remove(DEP_DEPENDENCY + f'final_adsb{day}_inter.json')

@app.route('/<date>/<specifed_file>', methods=['GET']) # type: ignore
def get_mdb_data(date: str, specifed_file: str):
    """Date will be in YYYY-MM-DD format, provided by the UI, then
    the file will be pulled from the database or cache, and returned to the UI"""

    results = collection.find_one({"_id": date})
    try:
        if results is None:
            log_main.critical("Data for %s not found in database", date)
            return Response(status=404, response=f'Data for {date} not found in database')
        else:
            log_main.info("Data for %s forwarded to UI", date)
            return Response(json.dumps(results[specifed_file], indent=2), content_type='application/json')
    except TypeError as error:
        log_main.critical(error)
        return Response(status=404, response='Invalid date format. Please use YYYY-MM-DD format.')

@app.route('/')
def default():
    """Default route"""
    return jsonify({'message': 'Welcome to the API!'})

@dataclass
class Analytics:
    """Dataclass for analytics, used to return data to the UI"""
    date: str = day

    ac_type = pd.Series(['EUFI', 'F16', 'V22', 'F18S', 'A10',
                        'F35LTNG', 'S61', 'H64', 'F15', 'AV8B', 'RC135'])
    callsign = pd.Series(['AF1', 'AF2'])
    er_flags = pd.Series(['7700', '7600', 'general', 'lifeguard',
                         'minfuel', 'nordo', 'unlawful', 'downed', 'reserved'])

    @classmethod
    def for_data(cls, date: str, info_req: str):
        """Date will be in YYYY-MM-DD format, provided by the UI"""
        t_data_frame = load_pd_data(date)

        try:
            log_main.info("%s data for %s fowarded to UI", info_req, cls.date)
            return pd.value_counts(t_data_frame[info_req]).to_dict()
        except KeyError:
            pass

    @classmethod
    def inter_ac(cls, date: str, row: str='t', data: str='ac_type'):
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
                return Response(status=404)

            d_file = t_data_frame[t_data_frame[row].isin(
                interesting_data)].to_dict(orient='records')
            log_main.info("Data written to 'final_adsb%s_inter.json'", date)
            return d_file
        except KeyError:
            log_main.critical(
                'Invalid data type. Please use ac_type, callsign or er_flags.')
            return Response(status=404)
