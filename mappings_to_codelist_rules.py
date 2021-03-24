import os
import json
from lxml import etree as ET

attrkey = '$'

def mapping_to_codelist_rules(mappings):
    for mapping in mappings.getroot().xpath('//mapping'):
        path_ref = mapping.find('path').text.split('@')
        # handle edge case of path: '//iati-activity/crs-add/channel-code/text()'
        if len(path_ref) != 2:
            split = mapping.find('path').text.rpartition('/')
            path_ref = [split[0] + split[1], split[2]]
        path = path_ref[0]
        attribute = path_ref[1]
        name = mapping.find('codelist').attrib['ref']
        file_name = name + '.xml'

        # get allowed codes into a list
        codelist = ET.parse(os.path.join('combined-xml', file_name))
        codes = codelist.getroot().xpath('//code')
        allowedCodes = []
        for code in codes:
            allowedCodes.append(code.text)

        out = {
            path: {
                attrkey: attribute,
                'codelist': file_name,
                'allowedCodes': allowedCodes
            }
        }

        # add condition
        if mapping.find('condition') is not None:
            out[path]['condition'] = mapping.find('condition').text

        # add validation rules
        validation_rules = mapping.find('validation-rules')
        if validation_rules is not None:
            for validation_rule in validation_rules:
                for child in validation_rule:
                    out[path][child.tag] = child.text  

        yield out


mappings = ET.parse('mapping.xml')
with open('codelist_rules.json', 'w') as fp:
    json.dump(list(mapping_to_codelist_rules(mappings)), fp)
