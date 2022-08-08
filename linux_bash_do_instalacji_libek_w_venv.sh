#!/bin/bash

path=$(pwd)
cd ..
cd skrypty_klraspi
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
cd $path
