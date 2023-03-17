#!/bin/bash

cd ..

cd ..

python -m ensurepip --upgrade

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
    npm install
fi

cd ..

if [ $? -eq 0 ]; then
    echo "Dependencies installed"
else
    echo "Failed to run"
    exit 1
fi