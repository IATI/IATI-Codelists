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
mkdir out/clv2
cp -r combined-xml out/clv2/xml

python gen.py
python old.py

python mappings_to_json.py
cp mapping.{xml,json} out/clv1/
cp mapping.{xml,json} out/clv2/

