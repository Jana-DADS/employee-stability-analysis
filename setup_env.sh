#!/usr/bin/env bash
set -e

# Create the virtual environment if it doesn't exist yet
if [ ! -d venv ]; then
    python3 -m venv venv
fi

source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Register a named Jupyter kernel so the notebook can be opened in this exact environment
python -m ipykernel install --user --name fluktuace --display-name "Python (fluktuace)"

echo ""
echo "Done. To use this environment:"
echo "  1. Activate it:   source venv/bin/activate"
echo "  2. In Jupyter or VS Code, select the kernel \"Python (fluktuace)\""
