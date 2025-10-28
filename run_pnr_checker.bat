@echo off
REM PNR Checker Batch Script
REM This script activates the environment and runs the PNR checker

cd /d "%~dp0"

REM Set environment variables for email notifications
set SEND_EMAIL=true

REM Run the Python script
python pnr_checker.py

REM Keep window open if there's an error (remove this line for silent execution)
REM pause
