python -m venv env
source env/bin/activate
pip download --dest modules --requirement requirements.txt
pip install --no-index --find-links=./modules -r requirements.txt
python setup.py
deactivate