@echo off
echo ================================================
echo  Setting up AutoDevCrew AI Environment (Windows)
echo ================================================
echo.

:: Create virtual environment
python -m venv venv
call venv\Scripts\activate

:: Upgrade pip
python -m pip install --upgrade pip

:: Install dependencies
echo Installing required packages...
pip install streamlit langchain pyautogen chromadb torch transformers fastapi uvicorn

:: Reminder for Ollama installation
echo ------------------------------------------------
echo Ollama is required for local AI model execution.
echo Please download and install it from: https://ollama.com/download
echo After installation, run:
echo     ollama pull llama3
echo ------------------------------------------------

echo.
echo ✅ AutoDevCrew environment setup completed successfully!
pause
