#!/bin/bash

rm -r out
mkdir out
cp -r xml out
mkdir out/json out/csv
python gen.py
