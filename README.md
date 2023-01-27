# adsb_mil_data
 
Creating a database for military aircraft. A GUI is in development and the end goal is an analytics application for military aircraft with both a realtime and historical datebase.

How to use: 

Create a ".env" file in the main directory with the format seen in ".env-sample"
Run app.py



ATTENTION: All information here is public. If there is a national security concern bring it up with ADBExchange not me.

If you somehow found this repo and wish to contribute to this atrocious code I based this on functional programming and the file system as of 1/26/23 is as follows:
api_proccessor.py: Conducts calls to the API, checks if API key and host are valid, and first round of data formatting. Status: Complete for now.

data_proccesor.py: Does the majority of the data processing, at the moment it removes objects that contain duplicate hex codes, objects containing the flight "TEST1234" as they are static VOR calibration beacons used by the FAA, and removes objects containing "GNDTEST". Status: Limited functionality, current priority with this module is ending the file that'll eventually be sent to a database, its most likely a quick fix. More details under the todo list in app.py. I'm still debating on the stats aspect of the project with the farthest I know being I want to use numpy.

test.py: As the name implies test.py is for testing and it's setup to allow the user to test individual functions within the aformentioned modules. Status: will scale as the project scales. Complete for now.

loggerConfig.py: Contains logging functions including a rollover function (Still WIP curently produces and error). Status: Working on that bug is the priority.

app.py: Final product meant to be run from here before the frontend is developed, when the frontend is created app.py will be depreciated. Status: Like test.py it will scale as the application does.

And yes I know the naming is trash I'll fix it soon.

In terms of contributing just open a PR with a small description of what you've done.