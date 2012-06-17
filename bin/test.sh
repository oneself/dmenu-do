#!/usr/bin/env bash

# Get the script's base directory
basedir=${0%/*}
cd "$basedir/../dmenudo/test"

nosetests --processes=2

if [ $? -ne 0 ]; then
    exit 1
fi
