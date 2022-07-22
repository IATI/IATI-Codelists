"""Script to turn codelist translations from the csv files into xml."""
from lxml import etree
import os
import io
import csv

# Output directories
OUTPUTDIR = ['', '']
# Path to the folder containing the csv files with translations
PATH_TO_CSV = ''
# Paths to the folders containing the embedded and nonembedded xml to be modified,
# ideally it should be the output folder for clv3 after running gen.sh
PATH_TO_XML = ["xml/", "IATI-Codelists-NonEmbedded/xml/"]
# ISO 639 language code in lowercase
LANG = ''


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


def get_xml_list(xml_path):
    """Get a list of xml files."""
    for a, b, files in os.walk(xml_path):
        return files


def write_narrative(xml, element, lang_string):
    """Write a new tag into the xml and adds the xml:lang attribute with the translated."""
    new_narrative = etree.Element("narrative")
    new_narrative.text = lang_string
    new_narrative.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = LANG
    element.append(new_narrative)


def get_codelist_item(code, xml):
    """Match the codelist-item within the xml to the code from the row in the csv."""
    for codelist_item in xml.findall('codelist-item'):
        if(code == codelist_item.find('code').text):
            return codelist_item


def is_translated(element, field):
    """Ensure that the element doesn't already have a translation."""
    for narrative in element.findall('narrative'):
        try:
            if narrative.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == LANG:
                # if there's already a french translation, rewrite it with the new one
                narrative.text = field
                return False
        except (KeyError):
            pass
    return True


def write_row(code, xml, name, description=''):
    """Write the contents of the csv row into the xml."""
    codelist_item = get_codelist_item(code, xml)
    if description != '':

        if is_translated(codelist_item.find('name'), name):
            write_narrative(xml, codelist_item.find('name'), name)
        if is_translated(codelist_item.find('description'), description):
            write_narrative(xml, codelist_item.find('description'), description)
        return 2
    else:
        if is_translated(codelist_item.find('name'), name):
            write_narrative(xml, codelist_item.find('name'), name)
        return 1


embedded_list = get_xml_list(PATH_TO_XML[0])
nonembedded_list = get_xml_list(PATH_TO_XML[1])
parser = etree.XMLParser(remove_blank_text=True)
for a, b, codelists in os.walk(PATH_TO_CSV):
    # Go through the csv filenames
    if not codelists:
        print("No CSV files were found")
    codelist_count = 0
    field_count = 0
    for codelist_csv in codelists:
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
                codelist_xml = etree.parse('{}{}.xml'.format(xml_path, codelist_name), parser)
                reader = csv.DictReader(csv_file)
                if "description ({})".format(LANG.upper()) in reader.fieldnames:
                    for row in reader:
                        field_count += write_row(
                            row['code'],
                            codelist_xml.find('codelist-items'),
                            row['name ({})'.format(LANG.upper())],
                            row['description ({})'.format(LANG.upper())]
                        )
                else:
                    for row in reader:
                        field_count += write_row(
                            row['code'],
                            codelist_xml.find('codelist-items'),
                            row['name ({})'.format(LANG.upper())]
                        )
            # Output the xml as new files matching the OUTPUTDIR
            indent(codelist_xml.getroot(), 0, 4)
            codelist_xml.write(os.path.join(output, '{}.xml'.format(codelist_name)), encoding='utf-8')
            codelist_count += 1
        except (OSError, IOError):
            print("{} codelist XML file not found".format(codelist_name))
    print("Translated {} fields in {}/{} codelists".format(field_count, codelist_count, len(codelists)))
