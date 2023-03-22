@echo off

cd %~dp0\..\..

python -m ensurepip --upgrade

pip install -r requirements.txt

if exist "dist" (
    echo dist exists
    rmdir /s /q dist
) else (
    echo dist does not exist
)

cd client

if exist "node_modules" (
    echo node_modules exists
) else (
    echo node_modules does not exist
    npm install
)

cd ..

if %errorlevel% equ 0 (
    echo Started, check log for more info on runtime events
) else (
    echo Failed to run, check if there is a requirements.txt file in the same directory as this script
    exit /b 1
)
