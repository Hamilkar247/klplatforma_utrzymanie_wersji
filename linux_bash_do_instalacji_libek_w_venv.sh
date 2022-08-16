#!/bin/bash

path=$(pwd)
echo $(pwd)
cd ..
echo $(pwd)
cd klplatforma_odbior_wysylka
echo "jestem w $(pwd)"
echo "virtualenv venv"
/usr/local/bin/virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
cd $path
