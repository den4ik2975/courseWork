@echo off

rem Check Python version
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.10 or higher.
    pause
    exit /b 1
)

python -c "import sys; exit(sys.version_info < (3, 10))" >nul 2>&1
if %errorlevel% neq 0 (
    echo Python version 3.10 or higher is required. Your current version is:
    python --version
    pause
    exit /b 1
)


rem Install requirements
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing requirements
    pause
    exit /b 1
)
echo Requirements installed successfully

rem Start main.py
python main.py
if %errorlevel% neq 0 (
    echo Error starting main.py
    pause
    exit /b 1
)
