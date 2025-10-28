@echo off
REM PNR Checker Batch Script
REM This script activates the environment and runs the PNR checker

REM Change to script directory
cd /d "%~dp0"

REM Load environment variables from .env file
for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
    if not "%%a"=="" if not "%%a:~0,1%"=="#" set "%%a=%%b"
)

REM Set email flag
set SEND_EMAIL=true

REM Run the Python script
python pnr_checker.py > pnr_checker.log 2>&1

REM Exit with the error code from Python
exit /b %ERRORLEVEL%
