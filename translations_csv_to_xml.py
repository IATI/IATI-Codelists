"""Script to turn codelist translations from the csv files into xml."""
from bs4 import BeautifulSoup
import os
import io
import csv

# Output directory
OUTPUTDIR = ""
# Path to the folder containing the csv files with translations
PATH_TO_CSV = ""
# Path to the folder containing the xml to be modified,
# ideally it should be the output folder for clv3 after running gen.sh
PATH_TO_XML = ""
# ISO 639 language code
LANG = ""


def write_narrative(xml, element, lang_string):
    """Write a new tag into the xml and adds the xml:lang attribute with the translated."""
    new_narrative = xml.new_tag("narrative")
    new_narrative.string = lang_string
    element.append(new_narrative)
    new_narrative['xml:lang'] = LANG


def get_codelist_item(code, xml):
    """Match the codelist-item within the xml to the code from the row in the csv."""
    for codelist_item in xml.findAll('codelist-item'):
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


for a, b, codelists in os.walk(PATH_TO_CSV):
    # Go through the csv filenames
    if not codelists:
        print("No CSV files were found")
    codelist_count = 0
    field_count = 0
    for codelist_csv in codelists:
        # Open xml and csv files by matching it to the csv filename
        codelist_name = os.path.splitext(codelist_csv)[0]
        try:
            with io.open(os.path.join(PATH_TO_XML, '{}.xml'.format(codelist_name))) as xml_file, io.open(os.path.join(PATH_TO_CSV, codelist_csv),'r', encoding="utf-8") as csv_file:
                codelist_xml = BeautifulSoup(xml_file, "lxml-xml")
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
            with open(os.path.join(OUTPUTDIR, '{}.xml'.format(codelist_name)), "w") as write_file:
                write_file.write(str(codelist_xml))
                codelist_count += 1
        except (OSError, IOError) as e:
            print("{} codelist XML file not found".format(codelist_name))
    print("Translated {} fields in {}/{} codelists".format(field_count, codelist_count, len(codelists)))
