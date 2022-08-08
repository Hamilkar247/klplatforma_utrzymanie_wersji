#!/bin/bash

deactivate
source "$1"/venv/bin/activate
pip3 install -r "$1"/requirements.txt

