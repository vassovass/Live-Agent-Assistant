@echo off

:: Set the project directory
set "PROJECT_DIR=C:\Users\vasso.vassiliades\Downloads\Live Agent Assistant\Live-Agent-Assistant"
set "AI_ASSISTANT_DIR=%PROJECT_DIR%\ai_assistant"
set "VENV_DIR=%PROJECT_DIR%\venv"

:: Change to the AI Assistant directory
echo Changing to AI Assistant directory...
cd /d "%AI_ASSISTANT_DIR%"
if errorlevel 1 (
    echo Failed to change directory. Please check if the path exists:
    echo %AI_ASSISTANT_DIR%
    pause
    exit /b 1
)
echo Successfully changed to AI Assistant directory.
echo Current directory: %CD%

:: Create virtual environment if it doesn't exist
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
)

:: Activate the virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)
echo Virtual environment activated successfully.

:: Output information about running requirements
echo.
echo To install dependencies, run the following command:
echo pip install -r requirements.txt

:: Keep the command prompt open
cmd /k
