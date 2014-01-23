#!/bin/bash

rm -rf combined-xml
if [ -d IATI-Codelists-External ]; then
    cd IATI-Codelists-External || exit 1
    git pull
    cd .. || exit 1
else
    git clone https://github.com/IATI/IATI-Codelists-External.git
fi

mkdir combined-xml
cp xml/* combined-xml
cp IATI-Codelists-External/xml/* combined-xml

rm -rf out
mkdir out
cp -r combined-xml out/xml
python gen.py
