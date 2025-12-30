@echo off
REM === Activate virtual environment, navigate to app folder, and run Streamlit ===

REM Path to project virtual environment
set VENV_PATH=D:\Documents\Etudes\Applications\nlp-file-converter\.nlp_file_converter_env

REM Path to Streamlit app folder
set APP_PATH=D:\Documents\Etudes\Applications\nlp-file-converter\nlp-demo-app

REM Name of Streamlit app file
set APP_FILE=app.py

REM Activate the virtual environment
call %VENV_PATH%\Scripts\activate.bat

REM Navigate to the app folder
cd /d %APP_PATH%

REM Run the Streamlit app
streamlit run %APP_FILE%

REM Keep the window open after execution
pause
