"""Script to add metadata/category to the codelists xml files."""
from bs4 import BeautifulSoup
import os
import io
import csv

# Output directory
OUTPUTDIR_CORE = ""
OUTPUTDIR_NON_CORE = ""
# Path to the csv with mapping
CSV_FILE = ""
# Paths to the folder containing the xml to be modified,
PATH_TO_XML = ""
# Version of the standard
VERSION = ""


def write_category(xml, metadata, category):
    """Write a new tag into the xml."""
    new_category = xml.new_tag("category")
    new_category.string = category
    metadata.append(new_category)


with io.open(os.path.join(CSV_FILE)) as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        if row['Type_version {}'.format(VERSION)] == "Embedded":
            try:
                with io.open(os.path.join(PATH_TO_XML, "{}.xml".format(row['Codelist']))) as xml_file, io.open(os.path.join(OUTPUTDIR_CORE, '{}.xml'.format(row['Codelist'])), "w") as write_file:
                    codelist_xml = BeautifulSoup(xml_file, "lxml-xml")
                    write_category(codelist_xml, codelist_xml.find('metadata'), "Core")
                    write_file.write(codelist_xml.prettify())
            except (OSError, IOError) as e:
                print("XML File {} does not exist".format(row['Codelist']))
        elif row['Type_version {}'.format(VERSION)] == "" or row['Type_version {}'.format(VERSION)] == "N/A":
            print("Codelist {} does not exist in version {}".format(row['Codelist'],VERSION))
        else:
            try:
                with io.open(os.path.join(PATH_TO_XML, "{}.xml".format(row['Codelist']))) as xml_file, io.open(os.path.join(OUTPUTDIR_NON_CORE, '{}.xml'.format(row['Codelist'])), "w") as write_file:
                    codelist_xml = BeautifulSoup(xml_file, "lxml-xml")
                    write_category(codelist_xml, codelist_xml.find('metadata'), row['New Type'])
                    write_file.write(codelist_xml.prettify())
            except (OSError, IOError) as e:
                print("XML File {} does not exist".format(row['Codelist']))
