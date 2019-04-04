from bs4 import BeautifulSoup
import os, io
import csv


OUTPUTDIR = os.path.join('french_codelists', 'fr_')
path_to_csv = 'translated_by_canada/'
path_to_xml = 'out/clv3/xml/'


def write_narrative(xml, element, fr_string):
    fr_narrative = xml.new_tag("narrative")
    fr_narrative.string = fr_string
    element.append(fr_narrative)
    fr_narrative['xml:lang'] = "fr"


def get_codelist_item(code, xml):
    for codelist_item in xml.findAll('codelist-item'):
        if(code == codelist_item.find('code').get_text()):
            return codelist_item


def not_translated(element):
    for narrative in element.findAll('narrative'):
        try:
            if narrative['xml:lang'] == "fr":
                return False
        except (KeyError):
            pass
    return True

for a, b, codelists in os.walk(path_to_csv):
    for codelist_csv in codelists:
        with open('{}{}.xml'.format(path_to_xml, (codelist_csv[:-4]))) as filename:
            codelist_xml = BeautifulSoup(filename, "lxml-xml")
            filepath = os.path.join(path_to_csv, codelist_csv)
            with io.open(filepath, 'r', encoding="ISO-8859-1") as filename:
                reader = csv.DictReader(filename)
                if "description (FR)" in reader.fieldnames:
                    for row in reader:
                        codelist_item = get_codelist_item(row['code'], codelist_xml)
                        if row['description (FR)'] != '':
                            if not_translated(codelist_item.find('name')):
                                write_narrative(codelist_xml, codelist_item.find('name'), row['name (FR)'])
                            if not_translated(codelist_item.find('description')):
                                write_narrative(codelist_xml, codelist_item.find('description'), row['description (FR)'])
                        else:
                            if not_translated(codelist_item.find('name')):
                                write_narrative(codelist_xml, codelist_item.find('name'), row['name (FR)'])
                else:
                    for row in reader:
                        codelist_item = get_codelist_item(row['code'], codelist_xml)
                        if not_translated(codelist_item.find('name')):
                            write_narrative(codelist_xml, codelist_item.find('name'), row['name (FR)'])
        with open("{}{}.xml".format(OUTPUTDIR, codelist_csv[:-4]), "w") as write_file:
            write_file.write(str(codelist_xml))
