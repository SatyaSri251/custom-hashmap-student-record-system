@echo off
title Custom HashMap Student Record System
echo ==========================================
echo   Custom HashMap Student Record System
echo ==========================================
echo.
where py >nul 2>nul
if %errorlevel%==0 (
    set PY=py
) else (
    set PY=python
)
if not exist venv (
    echo Creating virtual environment...
    %PY% -m venv venv
)
call venv\Scripts\activate.bat
echo Installing dependencies...
python -m pip install -r requirements.txt
echo.
echo Starting website...
echo Open http://127.0.0.1:5001 in your browser.
echo Press CTRL+C to stop.
python app.py
pause
