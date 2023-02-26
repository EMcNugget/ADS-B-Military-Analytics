"""Main function contains functionality for the API and the UI, as well as the MongoDB queries and data processing"""

import os
import datetime
import time
from dataclasses import dataclass
import pandas as pd
import requests
from flask import Flask, Response, jsonify, render_template
from flask_cors import CORS
from markupsafe import escape
from pymongo import MongoClient

API_KEY = os.environ["API_KEY"]
API_HOST = os.environ["API_HOST"]
MDB_URL = os.environ["MDB_URL"]
day = datetime.date.today().strftime('%Y-%m-%d')
cluster = MongoClient(MDB_URL)
db = cluster["milData"]
collection = db["historicalData"]
current_time = datetime.datetime.now().time()
app = Flask(__name__)
CORS(app)


def delay_time():
    """Sets the delay time based on the current time of day"""

    if datetime.time(4, 0) <= current_time <= datetime.time(19, 0):
        return 350
    elif datetime.time(19, 0) < current_time <= datetime.time(23, 59):
        return 750
    elif datetime.time(0, 1) < current_time <= datetime.time(3, 59):
        return 450
    else:
        return 550


def api_check():
    """Checks the API key and host to ensure they are valid"""

    data = get_data()
    if API_KEY is None or API_HOST is None:
        return False
    if data == '{"message":"You are not subscribed to this API."}':
        return False
    time.sleep(3)
    return True


def get_data():
    """Gets data from the API and returns it as a JSON object"""

    url = "https://adsbexchange-com1.p.rapidapi.com/v2/mil/"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    response = requests.request(
        "GET", url, headers=headers, timeout=3)  # type: ignore
    data = response.json()
    return data


@dataclass
class Main:
    """Class for main, used to return data to the UI"""

    main_data = {}
    post_data = {}
    date: str = day
    ac_type = pd.Series(['EUFI', 'F16', 'V22', 'F18S', 'A10',
                        'F35LTNG', 'S61', 'H64', 'F15', 'AV8B', 'RC135'])
    df = {'hex': [], 'flight': [], 't': [], 'r': []}

    @classmethod
    def pre_proccess(cls):
        """Removes duplicates and extraneous data"""

        for item in cls.main_data['ac']:
            hex_val = item['hex']
            if hex_val not in cls.df['hex']:
                cls.df['hex'].append(hex_val)
                cls.df['flight'].append(item.get('flight', 'None').strip())
                cls.df['t'].append(item.get('t', 'None'))
                cls.df['r'].append(item.get('r', 'None'))
        df_data = pd.DataFrame(cls.df)
        df_data.drop(df_data[df_data['r'] == 'TWR'].index, inplace=True)
        df_data.drop(df_data[df_data['t'] == 'GND'].index, inplace=True)
        df_data.drop(df_data[df_data['flight'] ==
                     'TEST1234'].index, inplace=True)
        return df_data.to_dict(orient='records')

    @classmethod
    def auto_req(cls):
        """Automatically requests data from the API and writes it to a JSON file
        at a specified interval as defined by the DELAY variable"""

        while True:
            cls.main_data.update(get_data())
            cls.pre_proccess()
            print("Data collected")
            time.sleep(delay_time())

    @classmethod
    def mdb_insert(cls):
        """Inserts data into MongoDB"""

        doc = {"_id": f"{day}", "data": cls.pre_proccess(
        ), "stats": cls.ac_count(), "inter": cls.inter_ac()}
        collection.insert_one(doc)
        print("Data inserted into MongoDB")

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
        if interesting_ac[interesting_ac['t'].isin(cls.ac_type)].to_dict(orient='records') == []:
            return jsonify({"message": "No interesting aircraft found"})


def rollover():
    """Checks the time every second and runs the mdb_insert function at 11:59:45pm"""

    while True:
        if datetime.datetime.now().strftime('%H:%M:%S') == '23:59:45':
            Main.mdb_insert()
        time.sleep(1)


@app.route('/<date>/<specified_file>', methods=['GET'])
def get_mdb_data(date: str, specified_file: str):
    """Date will be in YYYY-MM-DD format, provided by the UI, then
    the file will be pulled from the database or cache, and returned to the UI"""

    results = collection.find_one({"_id": date})
    try:
        if results is None:
            try:
                datetime.date.fromisoformat(date)
                return Response(status=400, response=f'Data for {escape(date)} not found in database')
            except ValueError:
                return Response(status=500, response='Invalid date format. Please use YYYY-MM-DD format.')
        else:
            try:
                response_data = results[specified_file]
            except KeyError:
                return Response(status=400, response=f'File {escape(specified_file)} not found for {escape(date)}')
            return jsonify(response_data)
    except TypeError:
        return Response(status=500, response='Invalid date format. Please use YYYY-MM-DD format.')


@app.route('/')
def default():
    """Default route"""
    return Response(status=400, response='Please specify a date and file')


@app.errorhandler(404)
def not_found(error_code):
    """404 error handler"""
    error_asset = os.path.join(os.path.dirname(__file__), 'templates/404.html')
    return render_template(error_asset), error_code
