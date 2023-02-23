#!/bin/bash

python -m ensurepip --upgrade

find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

if [ -f requirements.txt ]; then
    echo "requirements.txt found, skipping pipreqs"
else
    echo "requirements.txt not found, running pipreqs"
    pip install pipreqs
    pipreqs ./ --encoding=utf-8 --ignore .venv --force
fi

pip install -r requirements.txt

if [ -d "dist" ]; then
    echo "dist exists"
    rmdir dist
else
    echo "dist does not exist"
fi

cd client 

if [ -d "node_modules" ]; then
    echo "node_modules exists"
else
    echo "node_modules does not exist"
    npm install --force
fi

cd ..

if [ $? -eq 0 ]; then
    echo "Started, check log for more info on runtime events"
else
    echo "Failed to run, check if there is a requirements.txt file in the same directory as this script"
    exit 1
fi