@echo off

cd %~dp0\..\..

start cmd /k "py app.py"

start cmd /k "cd /d client && npm run dev"

start cmd /k "cd /d server && py main.py"
