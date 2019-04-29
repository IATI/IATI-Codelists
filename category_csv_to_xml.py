"""Script to add metadata/category to the codelists xml files."""
from lxml import etree
import os
import io
import csv

# Output directory
OUTPUTDIR_CORE = ""
OUTPUTDIR_NON_CORE = ""
# Path to the csv with mapping
CSV_FILE = ""
# Paths to the folder containing the xml to be modified,
PATH_TO_XML = "combined-xml/"
# Version of the standard
VERSION = "2.03"


def indent(elem, level=0, shift=2):
    """# Adapted from code at http://effbot.org/zone/element-lib.htm."""
    i = "\n" + level * " " * shift
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + " " * shift
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1, shift)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def write_category(xml, metadata, category):
    """Write a new tag into the xml."""
    new_category = etree.Element("category")
    new_narrative = etree.Element("narrative")
    new_narrative.text = category
    new_category.append(new_narrative)
    metadata.append(new_category)


with io.open(os.path.join(CSV_FILE)) as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        if row['Type_version {}'.format(VERSION)] == "Embedded":
            try:
                codelist_xml = etree.parse('{}/{}.xml'.format(PATH_TO_XML, row['Codelist']))
                write_category(codelist_xml, codelist_xml.find('metadata'), "Core")
                indent(codelist_xml.getroot(), 0, 4)
                codelist_xml.write(os.path.join(OUTPUTDIR_CORE, '{}.xml'.format(row['Codelist'])), encoding='utf-8')
            except (OSError, IOError):
                print("XML File {} does not exist".format(row['Codelist']))
        elif row['Type_version {}'.format(VERSION)] == "" or row['Type_version {}'.format(VERSION)] == "N/A":
            print("Codelist {} does not exist in version {}".format(row['Codelist'], VERSION))
        else:
            try:
                codelist_xml = etree.parse('{}/{}.xml'.format(PATH_TO_XML, row['Codelist']))
                write_category(codelist_xml, codelist_xml.find('metadata'), row['New Type'])
                indent(codelist_xml.getroot(), 0, 4)
                codelist_xml.write(os.path.join(OUTPUTDIR_NON_CORE, '{}.xml'.format(row['Codelist'])), encoding='utf-8')
            except (OSError, IOError):
                print("XML File {} does not exist".format(row['Codelist']))
