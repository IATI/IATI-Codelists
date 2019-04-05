"""Script to turn codelist translations from the csv files into xml."""
from bs4 import BeautifulSoup
import os
import io
import csv

# Output directory
OUTPUTDIR = ""
# Path to the folder containing the csv files with translations
path_to_csv = ""
# Path to the folder containing the xml to be modified,
# ideally it should be the output folder for clv3 after running gen.sh
path_to_xml = 'out/clv3/xml/'
# ISO 639 language code
lang = ""


def write_narrative(xml, element, lang_string, lang):
    """Write a new tag into the xml and adds the xml:lang attribute with the translated."""
    new_narrative = xml.new_tag("narrative")
    new_narrative.string = lang_string
    element.append(new_narrative)
    new_narrative['xml:lang'] = lang


def get_codelist_item(code, xml):
    """Match the codelist-item within the xml to the code from the row in the csv."""
    for codelist_item in xml.findAll('codelist-item'):
        if(code == codelist_item.find('code').get_text()):
            return codelist_item


def not_translated(element, lang):
    """Ensure that the element doesn't already have a translation."""
    for narrative in element.findAll('narrative'):
        try:
            if narrative['xml:lang'] == lang:
                return False
        except (KeyError):
            pass
    return True


def write_row(code, xml, name, lang, description=''):
    """Write the contents of the csv row into the xml."""
    codelist_item = get_codelist_item(code, xml)
    if description != '':
        if not_translated(codelist_item.find('name'), lang):
            write_narrative(xml, codelist_item.find('name'), name, lang)
        if not_translated(codelist_item.find('description'), lang):
            write_narrative(xml, codelist_item.find('description'), description, lang)
    else:
        if not_translated(codelist_item.find('name'), lang):
            write_narrative(xml, codelist_item.find('name'), name, lang)


for a, b, codelists in os.walk(path_to_csv):
    # Go through the csv filenames
    for codelist_csv in codelists:
        # Open xml files by matching it to the csv filename
        with open('{}{}.xml'.format(path_to_xml, (codelist_csv[:-4]))) as filename:
            codelist_xml = BeautifulSoup(filename, "lxml-xml")
            filepath = os.path.join(path_to_csv, codelist_csv)
            # Open the matching csv file
            with io.open(filepath, 'r', encoding="utf-8") as filename:
                reader = csv.DictReader(filename)
                if "description ({})".format(lang.upper()) in reader.fieldnames:
                    for row in reader:
                        write_row(row['code'], codelist_xml, row['name ({})'].format(lang.upper()), lang, row['description ({})'.format(lang.upper())])
                else:
                    for row in reader:
                        write_row(row['code'], codelist_xml, row['name ({})'].format(lang.upper()), lang)
        # Output the xml as new files matching the OUTPUTDIR
        with open("{}{}.xml".format(OUTPUTDIR, codelist_csv[:-4]), "w") as write_file:
            write_file.write(str(codelist_xml))
