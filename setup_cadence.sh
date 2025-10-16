#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <link to zipped google drive folder>"
    exit 1
fi

python3 -m venv cadence-env
source cadence-env/bin/activate
pip install --upgrade pip
pip install gdown

python setup_cadence.py "$1"