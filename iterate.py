import json
import os

file_path = os.path.dirname(os.path.realpath(__file__))
data2 = open(file_path + '/data/adsb.json', 'r').read()
db = json.loads(data2)

def data_set():
    for v in db['ac']:
        with open (file_path + '/data/test2.json', 'a') as file:
            mil_data = json.dumps(v, indent=4, separators=(',', ': '))
            mil_data += ",\n"
            return mil_data

def formatter():
    setup = 
    with open (file_path + '/data/test2.json', 'a') as file:
        file.write(setup)
formatter()