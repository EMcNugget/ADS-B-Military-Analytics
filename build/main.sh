#!/bin/bash

cd ..

python -m ensurepip --upgrade

pip install pipreqs

pipreqs ./ --encoding=utf-8 --ignore .venv --force

pip install -r requirements.txt

waitress-serve --host 127.0.0.1 --call main:MainClass.api_func

if [ $? -eq 0 ]; then
    echo "Started, check log for more info on runtime events"
else
    echo "Failed to run, check if there is a requirements.txt file in the same directory as this script"
    exit 1
fi