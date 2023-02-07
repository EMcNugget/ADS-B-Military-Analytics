# adsb_mil_data

Creating a database for military aircraft. A GUI is in development and the end goal is an analytics application for military aircraft with both a realtime and historical datebase.

**Requirements:**

NodeJS

Python

A valid ADSBExchange v2 API Key

**How to use:**

Create a .env file with the requirements as set in .env-sample. A further argument is require for the mongodb interaction. Please contact me via the discussions if you wish to obtain this otherwise it'll be kept private.

Manual way:

``` bash
python -m ensurepip --upgrade
pip install -r requirements.txt
```

Linux:

``` bash
./adsb_main.sh
````

**Then:**

``` bash
python -c app.py
```

Windows: Used the same way as linux (Make sure you have Git or a Unix emulator installed, or use the manual method)

Current stack is Django, and MongoDB

Planned additions to stack: Google Cloud, React.js, TailwindCSS, and PostCSS

**Current tasks:**

-Migrating to Pandas for data processing versus vanillia python

-Docker, makefile, etc to prevent the "It works on my machine" issue

**Known bugs:**

-DNS issue when connecting to MongoDB from some machines
