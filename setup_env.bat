@echo off
setlocal

REM Create the virtual environment if it doesn't exist yet
if not exist venv (
    python -m venv venv
)

call venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements.txt

REM Register a named Jupyter kernel so the notebook can be opened in this exact environment
python -m ipykernel install --user --name fluktuace --display-name "Python (fluktuace)"

echo.
echo Done. To use this environment:
echo   1. Activate it:   venv\Scripts\activate
echo   2. In Jupyter or VS Code, select the kernel "Python (fluktuace)"

endlocal
