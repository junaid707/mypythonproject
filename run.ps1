# PowerShell helper to create venv, install deps, and run the app
python -m venv venv
.
venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Run the Flask app
python app.py
