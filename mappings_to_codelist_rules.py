import os
import json
from lxml import etree as ET

def mapping_to_codelist_rules(mappings):
    data = dict()
    for mapping in mappings.getroot().xpath('//mapping'):
        path_ref = mapping.find('path').text.split('/@')
        # handle edge case of path: '//iati-activity/crs-add/channel-code/text()'
        if len(path_ref) != 2:
            split = mapping.find('path').text.rpartition('/')
            path_ref = [split[0], split[2]]
        path = path_ref[0]
        # change to direct reference paths
        path = path.replace('//iati-activities', '/iati-activities')
        path = path.replace('//iati-activity', '/iati-activities/iati-activity')
        path = path.replace('//iati-organisations', '/organisations')
        path = path.replace('//iati-organisation', '/iati-organisations/iati-organisation')

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
                attribute: {
                    'codelist': name,
                    'allowedCodes': allowedCodes
                }
            }
         }

        # add condition if present
        if mapping.find('condition') is not None:
            out[path][attribute]['condition'] = mapping.find('condition').text

        # add validation rules
        validation_rules = mapping.find('validation-rules')
        if validation_rules is not None:
            for validation_rule in validation_rules:
                for child in validation_rule:
                    out[path][attribute][child.tag] = child.text

        existingEntry = data.get(path)
        if existingEntry is not None:
            data[path][attribute] = out[path][attribute]  
        else:
            data.update(out)
    return data


mappings = ET.parse('mapping.xml')
with open('codelist_rules.json', 'w') as fp:
    data = mapping_to_codelist_rules(mappings)
    json.dump(data, fp)
