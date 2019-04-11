"""Script to turn codelist translations from the csv files into xml."""
from bs4 import BeautifulSoup
import os
import io
import csv
import re

# Output directories
OUTPUTDIR = ['', '']
# Path to the folder containing the csv files with translations
PATH_TO_CSV = 'translated_by_canada'
# Paths to the folders containing the embedded and nonembedded xml to be modified,
# ideally it should be the output folder for clv3 after running gen.sh
PATH_TO_XML = ["xml/", "IATI-Codelists-NonEmbedded/xml/"]
# ISO 639 language code in lowercase
LANG = 'fr'

orig_prettify = BeautifulSoup.prettify
regex = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter='minimal', indent_width=4):
    """Monkey patch for BeautifulSoup's prettifier."""
    return regex.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


BeautifulSoup.prettify = prettify


def get_xml_list(xml_path):
    """Get a list of xml files."""
    for a, b, files in os.walk(xml_path):
        return files


def write_narrative(xml, element, lang_string):
    """Write a new tag into the xml and adds the xml:lang attribute with the translated."""
    new_narrative = xml.new_tag("narrative")
    new_narrative.string = lang_string
    element.append(new_narrative)
    new_narrative['xml:lang'] = LANG


def get_codelist_item(code, xml):
    """Match the codelist-item within the xml to the code from the row in the csv."""
    codelists = xml.findAll('codelist-item')
    for codelist_item in codelists:
        if(code == codelist_item.find('code').get_text()):
            return codelist_item


def not_translated(element):
    """Ensure that the element doesn't already have a translation."""
    for narrative in element.findAll('narrative'):
        try:
            if narrative['xml:lang'] == LANG:
                return False
        except (KeyError):
            pass
    return True


def write_row(code, xml, name, description=''):
    """Write the contents of the csv row into the xml."""
    codelist_item = get_codelist_item(code, xml)
    if description != '':
        if not_translated(codelist_item.find('name')):
            write_narrative(xml, codelist_item.find('name'), name)
        if not_translated(codelist_item.find('description')):
            write_narrative(xml, codelist_item.find('description'), description)
        return 2
    else:
        if not_translated(codelist_item.find('name')):
            write_narrative(xml, codelist_item.find('name'), name)
        return 1

embedded_list = get_xml_list(PATH_TO_XML[0])
nonembedded_list = get_xml_list(PATH_TO_XML[1])
for a, b, codelists in os.walk(PATH_TO_CSV):
    # Go through the csv filenames
    if not codelists:
        print("No CSV files were found")
    codelist_count = 0
    field_count = 0
    for codelist_csv in codelists:
        # Open xml and csv files by matching it to the csv filename
        codelist_name = os.path.splitext(codelist_csv)[0]
        if "{}.xml".format(codelist_name) in embedded_list:
            xml_path = PATH_TO_XML[0]
            output = OUTPUTDIR[0]
        elif "{}.xml".format(codelist_name) in nonembedded_list:
            xml_path = PATH_TO_XML[1]
            output = OUTPUTDIR[1]
        else:
            print("{} codelist XML file not found".format(codelist_name))
            continue
        try:
            with io.open(os.path.join(PATH_TO_CSV, codelist_csv), 'r', encoding="utf-8") as csv_file:
                codelist_xml = BeautifulSoup(open(os.path.join(xml_path, '{}.xml'.format(codelist_name)), 'r'), 'lxml-xml')
                reader = csv.DictReader(csv_file)
                if "description ({})".format(LANG.upper()) in reader.fieldnames:
                    for row in reader:
                        field_count += write_row(
                            row['code'],
                            codelist_xml,
                            row['name ({})'.format(LANG.upper())],
                            row['description ({})'.format(LANG.upper())]
                        )
                else:
                    for row in reader:
                        field_count += write_row(
                            row['code'],
                            codelist_xml,
                            row['name ({})'.format(LANG.upper())]
                        )
            # Output the xml as new files matching the OUTPUTDIR
            with open(os.path.join(output, '{}.xml'.format(codelist_name)), "w") as write_file:
                xml_to_write = str(codelist_xml)
                write_file.write(xml_to_write)
                codelist_count += 1
        except (OSError, IOError) as e:
            print("{} codelist XML file not found".format(codelist_name))
    print("Translated {} fields in {}/{} codelists".format(field_count, codelist_count, len(codelists)))
