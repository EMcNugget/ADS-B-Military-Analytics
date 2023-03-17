#!/bin/bash

cd ..

cd ..

gnome-terminal --tab --title="App" --command="bash -c 'python3 app.py; $SHELL'"

gnome-terminal --tab --title="Client" --command="bash -c 'cd client && npm run dev; $SHELL'"

gnome-terminal --tab --title="Server" --command="bash -c 'cd server && python3 main.py; $SHELL'"

if [ $? -eq 0 ]; then
    echo "Started, check log for more info on runtime events"
else
    echo "Failed to run, check if there is a requirements.txt file in the same directory as this script"
    exit 1
fi