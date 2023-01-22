import requests
import logging
import os
import cred

log_directory = "data\\"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(level=logging.INFO, filename=os.path.join(
    log_directory, "adsb.json"), filemode='a')

url = "https://adsbexchange-com1.p.rapidapi.com/v2/mil/"
headers = {
    "X-RapidAPI-Key": cred.API_KEY,
    "X-RapidAPI-Host": cred.API_HOST
}


def get_data():
    response = requests.request("GET", url, headers=headers)
    logging.info(response.text)


while True:
    user = input("Enter a to request")
    try:
        if user == "a":
            print("Manual data requested")
            get_data()
        else:
            print("Invalid input")
    except Exception as e:
        print(e)
        logging.error(e)
