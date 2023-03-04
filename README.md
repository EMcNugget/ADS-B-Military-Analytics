# ADS-B Military Analytics

[![Deploy to Firebase Hosting](https://github.com/EMcNugget/adsb_mil_data/actions/workflows/firebase-hosting-merge.yml/badge.svg)](https://github.com/EMcNugget/adsb_mil_data/actions/workflows/firebase-hosting-merge.yml)
[![CodeQL](https://github.com/EMcNugget/adsb_mil_data/actions/workflows/codeql.yml/badge.svg)](https://github.com/EMcNugget/adsb_mil_data/actions/workflows/codeql.yml)

## What is this?

This allows you to view military aircraft from an ever growing database. Find out how many aircraft flew on a specific day, what type, among other features that are coming soon!

![Screenshot](/assets/demo.png)

## How To Run

1. Get an API key from ADSB Exchange (<https://www.adsbexchange.com/data/>)

2. Set your environment variables with said key and host with the following names: ```API_KEY``` and ```API_HOST``` respectively.

3. Run the following command in the root directory of the project: ```build.sh``` (This generates the dependencies for the client and server)

4. Then ```cd client``` and run ```npm run dev```

5. Then ```cd ../server``` and run ```python3 main.py```

6. Go to ```localhost:5173``` in your browser

## Notes

This project is currently in active development and is deployed at <https://adsbmilanalytics.com>

## Tech Stack

| Backend | Frontend |
| ------- | -------- |
| ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white) | ![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?style=flat&logo=typescript&logoColor=white) |
| ![MongoDB](https://img.shields.io/badge/-MongoDB-47A248?style=flat&logo=mongodb&logoColor=white) | ![React](https://img.shields.io/badge/-React-61DAFB?style=flat&logo=react&logoColor=white) |
| ![Google Cloud](https://img.shields.io/badge/-Google%20Cloud-4285F4?style=flat&logo=google-cloud&logoColor=white) | ![Vite](https://img.shields.io/badge/-Vite-646CFF?style=flat&logo=vite&logoColor=white) |
| | ![Firebase](https://img.shields.io/badge/-Firebase-FFCA28?style=flat&logo=firebase&logoColor=white)

## Current Tasks

See the project board for the current tasks. <https://github.com/users/EMcNugget/projects/6>

## Questions, Comments, Concerns?

Feel free to contact me at <support@adsbmilanalytics.com> or open an issue on the GitHub repo.
