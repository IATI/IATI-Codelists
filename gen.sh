#!/bin/bash

rm -rf IATI-Codelists-External combined-xml
git clone https://github.com/IATI/IATI-Codelists-External.git

mkdir combined-xml
cp xml/* combined-xml
cp IATI-Codelists-External/xml/* combined-xml

rm -rf out
mkdir out
cp -r xml out
python gen.py
