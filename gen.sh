#!/bin/bash

rm -rf out
mkdir out
cp -r xml out
mkdir out/json out/csv
python gen.py
