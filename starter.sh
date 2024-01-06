#!/bin/bash
echo It tries to install packages and set the python virtual env for you
echo Then run jupyter-notebook
pip3 install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
jupyter-notebook
deactivate