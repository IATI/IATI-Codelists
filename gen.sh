#!/bin/bash

rm -rf out
mkdir out
cp -r xml out
python gen.py
