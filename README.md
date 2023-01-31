# adsb_mil_data

Creating a database for military aircraft. A GUI is in development and the end goal is an analytics application for military aircraft with both a realtime and historical datebase.

**How to use:**

Create a .env file with the requirements as set in .env-sample. A further argument is require for the mongodb interaction. Please contact me via the discussions if you wish to obtain this otherwise it'll be kept private.

```
$ python -m ensurepip --upgrade
$ pip install -r requirements.txt
$ python -c app.py
```

ATTENTION: All information here is public. If there is a national security concern bring it up with ADBExchange not me. And yes I plan to update the file system soon.
And you need a valid API key for the ADSB Exchange API at the moment while everything is still in early development. When the project gets deployed to the web in the future this will no longer be a requirement.

Current stack is Python, MongoDB, and Google Cloud(WIP)

**Current tasks:**

-Migrating to Pandas for data processing versus vanillia python
-Docker, makefile, etc to prevent the "It works on my machine" issue

**Known bugs:**

-DNS issue when connecting to MongoDB from some machines
