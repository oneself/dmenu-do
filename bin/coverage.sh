#!/usr/bin/env bash

# Get the script's base directory
basedir=${0%/*}
cd "$basedir/../dmenudo/test"

nosetests  --processes=2 --with-coverage --cover-package=dmenudo --cover-erase --cover-inclusive --cover-html --cover-html-dir=../../cover

if [ $? -ne 0 ]; then
    exit 1
fi
