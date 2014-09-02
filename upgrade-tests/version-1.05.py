from __future__ import print_function
import sys
from lxml import etree as ET

#  
#  name: check_value_exists
#  @param filepath      Path to the codelist wee want to check
#  @param xpathString   xpath to the element we want to check
#  @param value         The value we want to check the existence of
#  @return yes/no
# 
def check_value_exists (filepath, xpathString, value):
  
  for items in ET.parse(filepath).getroot().findall('codelist-items'):
    values = items.xpath(xpathString)
    #print (', '.join(values))
    if value in values:
      print ('pass')
    else:
      print ('fail')

#  
#  name: check_value_does_not_exists
#  @param filepath      Path to the codelist wee want to check
#  @param xpathString   xpath to the element we want to check
#  @param value         The value we want to check does not exists
#  @return yes/no
#  

def check_value_does_not_exist (filepath, xpathString, value):
  
  for items in ET.parse(filepath).getroot().findall('codelist-items'):
    values = items.xpath(xpathString)
    #print (', '.join(values))
    if value in values:
      print ('fail')
    else:
      print ('pass')





#Test Description Type codelist changes
filepath = "../xml/DescriptionType.xml"
print (filepath)
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Other')
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','French Name') #Check for the translation value
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','4')
check_value_exists(filepath,'//codelist-items/codelist-item/description/text()','For miscellaneous use. A further classification or breakdown may be included in the narrative')

#Test Activity Status codelist changes
filepath = "../xml/ActivityStatus.xml"
print (filepath)
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Suspended')
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','French Name') #Check for the translation value
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','6')

#Test Transaction Type codelist changes
filepath = "../xml/TransactionType.xml"
print (filepath)
check_value_exists(filepath,'//codelist-items/codelist-item/description/text()','Funds received (whether from an external source or through internal accounting) for specific use on this activity.')

check_value_does_not_exist(filepath,'//codelist-items/codelist-item/description/text()','Funds received from an external funding source (eg a donor).')

#Test Related Activity Type codelist changes
filepath = "../xml/RelatedActivityType.xml"
print (filepath)
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Third Party') 
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','5')
check_value_exists(filepath,'//codelist-items/codelist-item/description/text()','A report by another organisation on the same activity (excluding activities reported as part of financial transactions - eg. provider-activity-id - or a multi-funded activity using code = 4)')

#Test DocumentCategory codelist changes
filepath = "../xml/DocumentCategory.xml"
print (filepath)
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Sector strategy') 
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','B11')
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Thematic strategy') 
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','B12')
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Country-level Memorandum of Understanding') 
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','B13')
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Evaluations policy') 
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','B14')
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','General Terms and Conditions') 
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','B15')
