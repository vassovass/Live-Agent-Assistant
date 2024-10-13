@echo off
echo Activating virtual environment and changing to AI Assistant directory...

cd /d C:\Users\vasso.vassiliades\Downloads\Live Agent Assistant\ai_assistant

if not exist ..\venv\Scripts\activate.bat (
    echo Virtual environment not found. Please create it first.
    pause
    exit /b 1
)

call ..\venv\Scripts\activate.bat

if errorlevel 1 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

echo Virtual environment activated successfully.
echo Current directory: %CD%
echo You are now in the AI Assistant virtual environment and correct folder.
echo.
echo To deactivate the virtual environment when you're done, type: deactivate
echo To start the application, type: python ai_assistant\main.py

cmd /k