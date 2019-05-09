from lxml import etree as ET
import os
import re
import csv
import json
from functools import partial

languages = ['en', 'fr']

xml_lang = '{http://www.w3.org/XML/1998/namespace}lang'

OUTPUTDIR = os.path.join('out', 'clv2')


def normalize_whitespace(x):
    if x is None:
        return x
    x = x.strip()
    x = re.sub(r'\s+', ' ', x)
    return x


def codelist_item_todict(codelist_item, default_lang='', lang='en'):
    out = dict([(child.tag, normalize_whitespace(child.text)) for child in codelist_item if child.tag not in ['name', 'description'] or child.attrib.get(xml_lang) == lang or (child.attrib.get(xml_lang) is None and lang == default_lang)])
    if 'public-database' in codelist_item.attrib:
        out['public-database'] = True if codelist_item.attrib['public-database'] in ['1', 'true'] else False
    return out


for language in languages:
    codelists = ET.Element('codelists')
    codelists_list = []

    try:
        os.makedirs(os.path.join(OUTPUTDIR, 'json', language))
        os.makedirs(os.path.join(OUTPUTDIR, 'csv', language))
    except OSError:
        pass

    for fname in os.listdir('combined-xml'):
        codelist = ET.parse(os.path.join('combined-xml', fname))
        attrib = codelist.getroot().attrib
        assert attrib['name'] == fname.replace('.xml', '')

        default_lang = codelist.getroot().attrib.get(xml_lang)
        codelist_dicts = list(partial(codelist_item_todict, default_lang=default_lang, lang=language), codelist.getroot().find('codelist-items').findall('codelist-item'))

        fieldnames = [
            'code',
            'name',
            'description',
            'category',
            'url'
        ]

        if fname == 'OrganisationRegistrationAgency.xml':
            fieldnames.append('public-database')

        dw = csv.DictWriter(open(os.path.join(OUTPUTDIR, 'csv', language, attrib['name'] + '.csv'), 'w'), fieldnames)
        dw.writeheader()
        for row in codelist_dicts:
            dw.writerow(row)

        name_elements = codelist.getroot().xpath('/codelist/metadata/name[{}@xml:lang="{}"]'.format('not(@xml:lang) or ' if language == default_lang else '', language))
        description_elements = codelist.getroot().xpath('/codelist/metadata/description[{}@xml:lang="{}"]'.format('not(@xml:lang) or ' if language == default_lang else '', language))
        url_elements = codelist.getroot().xpath('/codelist/metadata/url')

        # JSON
        json.dump(
            {
                'attributes': {
                    'name': attrib['name'],
                    'complete': attrib.get('complete'),
                    'embedded': attrib.get('embedded'),
                    'category-codelist': attrib.get('category-codelist'),
                },
                'metadata': {
                    'name': name_elements[0].text if name_elements else '',
                    'description': description_elements[0].text if description_elements else '',
                    'url': url_elements[0].text if url_elements else ''
                },
                'data': codelist_dicts
            },
            open(os.path.join(OUTPUTDIR, 'json', language, attrib['name'] + '.json'), 'w')
        )
        codelists_list.append(attrib['name'])

        ET.SubElement(codelists, 'codelist').attrib['ref'] = attrib['name']

tree = ET.ElementTree(codelists)
tree.write(os.path.join(OUTPUTDIR, 'codelists.xml'), pretty_print=True)

json.dump(codelists_list, open(os.path.join(OUTPUTDIR, 'codelists.json'), 'w'))
