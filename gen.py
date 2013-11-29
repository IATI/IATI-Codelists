from lxml import etree as ET
import os, json
import csv
from functools import partial

xml_lang = '{http://www.w3.org/XML/1998/namespace}lang'

def codelist_item_todict(codelist_item, default_lang='', lang='en'):
    return dict([ (child.tag, child.text) for child in codelist_item if child.attrib.get(xml_lang) == lang or (child.attrib.get(xml_lang) == None and lang == default_lang) ])

def utf8_encode_dict(d):
    def enc(a):
        if a is None: return None
        else: return a.encode('utf8')
    return dict( (enc(k), enc(v)) for k, v in d.items() )

codelists = ET.Element('codelists')
codelists_list = []

for fname in os.listdir('xml'):
    codelist = ET.parse(os.path.join('xml',fname))
    attrib = codelist.getroot().attrib
    assert attrib['name'] == fname.replace('.xml','')

    default_lang = codelist.getroot().attrib.get(xml_lang)
    codelist_dicts = map(partial(codelist_item_todict, default_lang=default_lang), codelist.getroot().findall('codelist-item'))

    ## CSV
    # TODO take this directly from scheam
    fieldnames = [
        'code',
        'name',
        'description',
        'category',
        'sector',
    ]
    dw = csv.DictWriter(open('out/csv/{0}.csv'.format(attrib['name']), 'w'), fieldnames)
    dw.writeheader()
    for row in codelist_dicts:
        dw.writerow(utf8_encode_dict(row))

    ## JSON
    json.dump(
        {
            'header': attrib['name'],
            'data': codelist_dicts
        },
        open('out/json/{0}.json'.format(attrib['name']), 'w')
    )
    codelists_list.append(attrib['name'])

    ET.SubElement(codelists, 'codelist').attrib['ref'] = attrib['name']

tree = ET.ElementTree(codelists)
tree.write("out/codelists.xml", pretty_print=True)

json.dump(codelists_list, open('out/codelists.json', 'w'))

