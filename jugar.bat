@echo off
echo Ejecutando Mario Bros...
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python main.py
pause
