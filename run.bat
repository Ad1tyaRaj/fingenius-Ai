@echo off
echo Starting AI Agent Team Web Application...
cd %~dp0
call Venv\Scripts\activate.bat

echo Installing required dependencies...
pip install -r requirements.txt

echo Starting the application...
python app.py
pause 