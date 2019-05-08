#!/bin/bash

rm -rf combined-xml
if [ -d IATI-Codelists-NonEmbedded ]; then
    cd IATI-Codelists-NonEmbedded || exit 1
    git pull
    git checkout python-3-upgrade
else
    git clone https://github.com/IATI/IATI-Codelists-NonEmbedded.git
    cd IATI-Codelists-NonEmbedded ||exit 1
    git checkout python-3-upgrade
fi
cd .. || exit 1

mkdir combined-xml
cp xml/* combined-xml
for f in IATI-Codelists-NonEmbedded/xml/*; do
    python v3tov2.py $f > combined-xml/`basename $f`;
done

rm -rf out
mkdir out
mkdir out/clv2
cp -r combined-xml out/clv2/xml

python gen.py
python old.py

python mappings_to_json.py
cp mapping.{xml,json} out/clv1/
cp mapping.{xml,json} out/clv2/

