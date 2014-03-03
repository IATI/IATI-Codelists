from __future__ import print_function
from lxml import etree as ET
from lxml.builder import E
from gen import languages
import os
import datetime, pytz

language = 'en'

try:
    os.makedirs(os.path.join('out','old'))
except OSError: pass

for fname in os.listdir('combined-xml'):
    codelist = ET.parse(os.path.join('combined-xml',fname))
    attrib = codelist.getroot().attrib
    old_codelist = E.codelist(**{
            'name':attrib['name'],
            'date-last-modified': datetime.datetime.now(pytz.utc).isoformat(),
            'version':'',
            '{http://www.w3.org/XML/1998/namespace}lang':language,
        })
    for codelist_item in codelist.getroot().find('codelist-items').findall('codelist-item'):
        old_codelist_item = E(attrib['name'],
            E.code(codelist_item.xpath('code[not(xml:lang) or xml:lang="en"]')[0].text),
            E.name(codelist_item.xpath('name[not(xml:lang) or xml:lang="en"]')[0].text),
            E.language(language)
            )

        if codelist_item.xpath('description[not(xml:lang) or xml:lang="en"]'):
            description = codelist_item.xpath('description[not(xml:lang) or xml:lang="en"]')[0].text
            if description:
                old_codelist_item.append(E.description(description))

        category = codelist_item.find('category')
        if category is not None:
            old_codelist_item.append(E('category', category.text))

        old_codelist.append(old_codelist_item)
    ET.ElementTree(old_codelist).write(os.path.join('out','old',fname), pretty_print=True)

