@echo off
REM PNR Checker Batch Script
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat

REM Run the Python script
python pnr_checker.py

exit /b %ERRORLEVEL%
