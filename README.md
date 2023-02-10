# adsb_mil_data

Creating a database for military aircraft. A GUI is in development and the end goal is an analytics application for military aircraft with both a realtime and historical datebase.

**How to use:**

Create a .env file with the requirements as set in .env-sample. A further argument is require for the mongodb interaction. Please contact me via the discussions if you wish to obtain this otherwise it'll be kept private.

Manual way:

```
$ python -m ensurepip --upgrade
$ pip install -r requirements.txt
$ python -c app.py
```

Linux:

```
./adsb_main.sh
````

Windows: Used the same way as linux (Make sure you have Git or a Unix emulator installed, or use the manual method)

ATTENTION: All information here is public.
All you need a valid API key for the ADSB Exchange API at the moment while everything is still in early development. When the project gets deployed to the web in the future this will no longer be a requirement.

Current stack is Python, MongoDB, and Google Cloud(WIP)

**Current tasks:**

-Migrating to Pandas for data processing versus vanillia python **DONE**

-Docker, makefile, etc to prevent the "It works on my machine" issue

-Flask REST API

**Known bugs:**

No known bugs that don't have to do with incompletion of a piece of code.
