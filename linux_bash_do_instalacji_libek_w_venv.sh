#!/bin/bash

path=$(pwd)
cd ..
cd klplatforma_odbior_wysylka
echo "jestem w $(pwd)"
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
cd $path
