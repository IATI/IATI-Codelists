from __future__ import print_function
from lxml import etree as ET
from lxml.builder import E
from gen import languages
from collections import OrderedDict
import os
import datetime, pytz
import json, csv

language = 'en'

try:
    os.makedirs(os.path.join('out','old'))
except OSError: pass

def utf8_encode_dict(d):
    def enc(a):
        if a is None: return None
        else: return a.encode('utf8')
    return dict( (enc(k), enc(v)) for k, v in d.items() )

for fname in os.listdir('combined-xml'):
    codelist = ET.parse(os.path.join('combined-xml',fname))
    attrib = codelist.getroot().attrib
    old_codelist_json = OrderedDict({
            'name':attrib['name'],
            'date-last-modified': datetime.datetime.now(pytz.utc).isoformat(),
            'version':'',
            '{http://www.w3.org/XML/1998/namespace}lang':language,
        })
    old_codelist = E.codelist(**old_codelist_json)
    del(old_codelist_json['{http://www.w3.org/XML/1998/namespace}lang'])
    old_codelist_json['xml:lang'] = language

    old_codelist_json_list = []
    for codelist_item in codelist.getroot().find('codelist-items').findall('codelist-item'):
        code = codelist_item.xpath('code[not(xml:lang) or xml:lang="en"]')[0].text
        name = codelist_item.xpath('name[not(xml:lang) or xml:lang="en"]')[0].text
        old_codelist_item = E(attrib['name'],
            E.code(code),
            E.name(name),
            E.language(language)
            )
        old_codelist_json_item = {
            'code':code,
            'name':name,
            'language':language
        }

        if codelist_item.xpath('description[not(xml:lang) or xml:lang="en"]'):
            description = codelist_item.xpath('description[not(xml:lang) or xml:lang="en"]')[0].text
            if description:
                old_codelist_item.append(E.description(description))
                old_codelist_json_item['description'] = description

        category = codelist_item.find('category')
        if category is not None:
            old_codelist_item.append(E('category', category.text))
            old_codelist_json_item['category'] = category.text

            category_item = ET.parse(os.path.join('combined-xml',attrib['category-codelist']+'.xml')).xpath('//codelist-item[code="{0}"]'.format(category.text))[0]

            category_name = category_item.xpath('name[not(xml:lang) or xml:lang="en"]')[0].text
            old_codelist_item.append(E('category-name', category_name))
            old_codelist_json_item['category-name'] = category_name

            if category_item.xpath('description[not(xml:lang) or xml:lang="en"]'):
                category_description = category_item.xpath('description[not(xml:lang) or xml:lang="en"]')[0].text
                if category_description:
                    old_codelist_item.append(E('category-description', category_description))
                    old_codelist_json_item['category-description'] = category_description

        old_codelist.append(old_codelist_item)
        old_codelist_json_list.append(old_codelist_json_item)

    with open(os.path.join('out','old',attrib['name']+'.csv'), 'w') as fp:
        dictwriter = csv.DictWriter(fp, ['code','name','description','language','category','category-name','category-description'])
        dictwriter.writeheader()
        for line in old_codelist_json_list:
            dictwriter.writerow(utf8_encode_dict(line))

    ET.ElementTree(old_codelist).write(os.path.join('out','old',fname), pretty_print=True)
    with open(os.path.join('out','old',attrib['name']+'.json'), 'w') as fp:
        old_codelist_json[attrib['name']] = old_codelist_json_list
        json.dump(old_codelist_json, fp)

