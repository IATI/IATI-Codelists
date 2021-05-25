import os
from lxml import etree as ET
import csv

mappings = ET.parse('mapping.xml')
headers = ['ID', 'Category', 'Severity', 'Codelist', 'Message', 'Context (Xpath)']
with open('codelist_rules.csv', 'w') as fp:
    writer = csv.writer(fp)
    writer.writerow(headers)

    for mapping in mappings.getroot().xpath('//mapping'):
        ID = ''
        category = ''
        severity = ''
        codelist = ''
        message = ''
        xpath = ''

        path = mapping.find('path').text
        codelist = mapping.find('codelist').attrib['ref']

        # add condition into xpath if present
        if (mapping.find('condition') is not None):
            condition = mapping.find('condition').text
            xpath = path.split('/@code')[0] + "[" + condition + "]" + '/@code'
        else:
            xpath = path

        # pull out validation rules
        validation_rules = mapping.find('validation-rules')
        if (validation_rules is None):
            raise Exception("No validation rules detected for codelist: " + codelist + " and xpath: " + xpath)
        if validation_rules is not None:
            # We can only handle a single rule per codelist currently
            for validation_rule in validation_rules:
                for child in validation_rule:
                    if (child.tag == 'id'):
                        ID = child.text
                    if (child.tag == 'severity'):
                        severity = child.text
                    if (child.tag == 'category'):
                        category = child.text
                    if (child.tag == 'message'):
                        message = child.text
                writer.writerow([ID, category, severity, codelist, message, xpath])


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

        existingPath = data.get(path) is not None
        existingPathAtr = ''
        if existingPath:
            existingPathAtr = data[path].get(attribute) is not None
        out = {
            path: {
                attribute: {
                }
            }
        }
        if (mapping.find('condition') is not None):
            # parse condition xpath
            condition = mapping.find('condition').text
            parts = condition.split(' or ')
            splitfirst = parts[0].split(' = ')
            link = splitfirst[0].lstrip('@')
            linkValue = splitfirst[1].strip("'")
            # import pdb; pdb.set_trace() # debugging code

            defaultLink = ''
            if len(parts) > 1:
                defaultLink = linkValue

            if not existingPath or not existingPathAtr:
                out[path][attribute]["conditions"] = {}
                out[path][attribute]["conditions"]["mapping"] = {}
                out[path][attribute]["conditions"]["linkedAttribute"] = link
            elif data[path][attribute].get("conditions") is None:
                out[path][attribute]["conditions"] = {}
                out[path][attribute]["conditions"]["mapping"] = {}
                out[path][attribute]["conditions"]["linkedAttribute"] = link
            else:
                out[path][attribute]["conditions"] = data[path][attribute]["conditions"]
            if defaultLink:
                out[path][attribute]["conditions"]["defaultLink"] = defaultLink

            out[path][attribute]["conditions"]["mapping"][linkValue] = {"codelist": name, "allowedCodes": allowedCodes}
        else:
            out[path][attribute]["codelist"] = name
            out[path][attribute]["allowedCodes"] = allowedCodes

        # add validation rules
        validation_rules = mapping.find('validation-rules')
        if validation_rules is not None:
            for validation_rule in validation_rules:
                for child in validation_rule:
                    if mapping.find('condition') is not None:
                        out[path][attribute]["conditions"]["mapping"][linkValue][child.tag] = child.text
                    else:
                        out[path][attribute][child.tag] = child.text
        if existingPath:
            data[path][attribute] = out[path][attribute]
        else:
            data.update(out)
    return data
