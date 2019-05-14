from os.path import join
from lxml import etree


org_id_xml = etree.parse(join('source', 'org-id-guide.xml'))
codelist_items = org_id_xml.find('codelist-items')

template = etree.parse(
    join('templates', 'OrganisationRegistrationAgency.xml'))
placeholder_codelist_items = template.find('codelist-items')

template.getroot().replace(placeholder_codelist_items, codelist_items)

template.write(
    join('xml', 'OrganisationRegistrationAgency.xml'),
    pretty_print=True)
