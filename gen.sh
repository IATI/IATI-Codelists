#!/bin/bash

rm -rf combined-xml
if [ -d IATI-Codelists-NonEmbedded ]; then
    cd IATI-Codelists-NonEmbedded || exit 1
    git pull
    cd .. || exit 1
else
    git clone https://github.com/IATI/IATI-Codelists-NonEmbedded.git
fi

mkdir combined-xml
cp xml/* combined-xml
cp IATI-Codelists-NonEmbedded/xml/* combined-xml

rm -rf out
mkdir out
cp -r combined-xml out/xml
python gen.py
