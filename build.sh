#!/bin/bash

python -m ensurepip --upgrade

if [ -f requirements.txt ]; then
    echo "requirements.txt found, skipping pipreqs"
else
    echo "requirements.txt not found, running pipreqs"
    pip install pipreqs
    pipreqs ./ --encoding=utf-8 --ignore .venv --force
fi

pip install -r requirements.txt

npm install

if [ $? -eq 0 ]; then
    echo "Started, check log for more info on runtime events"
else
    echo "Failed to run, check if there is a requirements.txt file in the same directory as this script"
    exit 1
fi