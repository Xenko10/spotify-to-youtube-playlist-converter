@echo off
echo Setting up Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment.
    exit
)
echo Virtual environment created successfully.

echo Installing requirements...
call venv\Scripts\activate
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements.
    exit
)
echo Requirements installed successfully.

echo Setup completed.
exit