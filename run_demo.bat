@echo off
setlocal
cd /d "%~dp0"

set "PYTHONPATH=%CD%"
set "PYTHONUTF8=1"

echo Project root: %CD%
echo PYTHONPATH: %PYTHONPATH%

echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 goto error

call .venv\Scripts\activate
if errorlevel 1 goto error

echo Installing dependencies...
python -m pip install --upgrade pip
if errorlevel 1 goto error

python -m pip install -r requirements.txt
if errorlevel 1 goto error

echo Starting Redpanda...
docker compose up -d
if errorlevel 1 goto error

echo Running local sample demo...
python scripts\generate_sample_source.py --rows 1000 --month 2024-01
if errorlevel 1 goto error

python scripts\main.py --mode full
if errorlevel 1 goto error

python scripts\main.py --mode check
if errorlevel 1 goto error

echo.
echo Demo finished successfully.
pause
exit /b 0

:error
echo.
echo ERROR: Demo failed. Check the error message above.
pause
exit /b 1