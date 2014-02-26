from lxml import etree as ET
import os, json

def mapping_to_json(mappings):
    for mapping in mappings.getroot().xpath('//mapping'):
        yield {
            'path': mapping.find('path').text,
            'codelist': mapping.find('codelist').attrib['ref']
        }

mappings = ET.parse('mapping.xml')
with open('mapping.json', 'w') as fp:
    json.dump(list(mapping_to_json(mappings)), fp)

