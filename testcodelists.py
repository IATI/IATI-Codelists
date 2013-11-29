import sys
from lxml import etree as ET

if len(sys.argv) < 2:
    print('Usage python testcodelists.py file.xml [mapping.xml]')
    exit()

if len(sys.argv) > 2:
    mapping_file = sys.argv[2]
else:
    mapping_file = 'mapping.xml'

root = ET.parse(sys.argv[1]).getroot()

for mapping in ET.parse(mapping_file).getroot().findall('mapping'):
    codelist_name = mapping.find('codelist').attrib['ref']
    codelist = ET.parse('xml/{0}.xml'.format(codelist_name))
    codes = [ x.text for x in codelist.xpath('//code') ]
    if mapping.find('base') is not None:
        bases = root.xpath(mapping.find('base').text)
    else:
        bases = [ root ]
    for base in bases:
        if mapping.find('condition') is not None:
            if not base.xpath(mapping.find('condition').text):
                print(base.xpath(mapping.find('condition').text))
                continue
        for code in base.xpath(mapping.find('path').text):
            if not code in codes:
                print('{0} not in {1}'.format(code, codelist_name))
