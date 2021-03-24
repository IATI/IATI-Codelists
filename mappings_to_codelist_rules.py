import json
from lxml import etree as ET

attrkey = '$'

def mapping_to_codelist_rules(mappings):
    for mapping in mappings.getroot().xpath('//mapping'):
        path_ref = mapping.find('path').text.split('@')
        # handles edge case of path: '//iati-activity/crs-add/channel-code/text()'
        if len(path_ref) != 2:
            split = mapping.find('path').text.rpartition('/')
            path_ref = [split[0] + split[1], split[2]]
            print(path_ref)
        out = {
            path_ref[0]: {
                attrkey: path_ref[1],
                'codelist': mapping.find('codelist').attrib['ref']
            }
        }
        if mapping.find('condition') is not None:
            out[path_ref[0]]['condition'] = mapping.find('condition').text

        yield out


mappings = ET.parse('mapping.xml')
with open('codelist_rules.json', 'w') as fp:
    json.dump(list(mapping_to_codelist_rules(mappings)), fp)
