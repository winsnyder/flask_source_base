#!/bin/bash

# Activate enviroment
source venv/bin/activate

# Define enviroment for application
export FLASK_ENV=development

export FLASK_APP=main.py

echo "Run application ..."
flask run