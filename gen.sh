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
for f in IATI-Codelists-NonEmbedded/xml/*; do
    python v3tov2.py $f > combined-xml/`basename $f`;
done

rm -rf out
mkdir out
mkdir -p out/clv2 out/clv3/xml
cp -r combined-xml out/clv2/xml

for f in combined-xml/*; do
    python v2tov3.py $f > out/clv3/xml/`basename $f`;
done


python gen.py
python v2tov1.py

cp -r out/clv2/{codelists.json,codelists.xml,csv,json} out/clv3/

python mappings_to_json.py
cp mapping.{xml,json} out/clv1/
cp mapping.{xml,json} out/clv2/
cp mapping.{xml,json} out/clv3/

