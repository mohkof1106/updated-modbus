import os.path
import xml.etree.ElementTree as ET
import math
import logging
logger = logging.getLogger("live_control")

from django.core.management.base import BaseCommand

from modbus_controller.settings import TEMPLATE_DIR
from controller_setup.models import AddressMapping, Template, Document, Table
from controller_setup.tools import crawl

def find_xml_path(template):
    "xml name as in the folder ex: AE 3TL Inverter (w/ or w/out .xml)"
    xml_name = template.file_name
    if not xml_name.endswith(".xml"):
        xml_name += ".xml"
    return os.path.join(TEMPLATE_DIR, xml_name)

def create_mapping(_template, _address, _label, _table, _factor, _unit):
    is_competitor = True # initialize
    try: # try to find if the mapping already exists and if so, logger.debug it
        mapping = AddressMapping.objects.filter(template=_template).filter(address=_address).get(table=_table)
        logger.debug("The mapping already exists %s" % mapping)
    except AddressMapping.DoesNotExist:
        is_competitor = False # passed the first test

    # if the mapping does not exist yet, verify if no one is occupying the same address with the same block_type (remember block type is the call function)
    for competitor_mapping in AddressMapping.objects.filter(template=_template).filter(address=_address):
        if competitor_mapping.table.block_type == _table.block_type:
            is_competitor = True
            logger.warning("Found competitor mapping with same template %s, address %s and block type %s" % (_template, _address, _table.block_type))
    if not is_competitor:
        mapping = AddressMapping(address=_address, label=_label, table=_table, \
            factor=_factor, unit=_unit, template=_template)
        logger.info("Created new mapping %s" % mapping)
        mapping.save()

def find_template_from_file_name(template_name):
    return Template.objects.get(file_name=template_name)
    
def create_mappings_to_template_from_xml(template):
    """Examples below, for a string we attrib multiple becomes the factor
      <Point id="1161514" name="02 -Length of model %2860 %3F%29">
         <Type>ShowValue</Type>
         <Address format="U16" index="40210" type="Holding"/>
         <Calculate/>
         <Enum/>
      </Point>
      <Point id="1161178" name="19 - Apparent Power" unit="VA">
         <Type>ShowValue</Type>
         <Address format="U16" index="40089" type="Holding"/>
         <Calculate scaling="0.1"/>
         <Enum/>
      <Point id="1222862" name="03 - SN">
         <Type>ShowValue</Type>
         <Address format="String" index="4990" multiple="10" type="Input"/>
         <Calculate/>
         <Enum/>
      </Point>
      """
    xml_path = find_xml_path(template)
    tree = ET.parse(xml_path)
    root = tree.getroot()
    points = root.iter('Point')
    unmapped = []
    for point in points:
        try:
            label = point.attrib["name"]
        except:
            label = "undf label"
        try:
            unit = point.attrib["unit"]
        except:
            unit = "undf unit"
        address_el = point.find("Address")
        if address_el is None:
            print point, point.attrib
            continue
        address = int(address_el.attrib["index"])
        try:
            reg_type = address_el.attrib["type"]
            table_format = address_el.attrib["format"]
            table = Table.link_format2table(reg_type, table_format)
        except Exception as e:
            # TODO: what default?
            print e, label, address_el.attrib
            unmapped.append(("passed", str(e), label, str(address_el.attrib)))
            continue
        try:
            factor = float(point.find("Calculate").attrib["scaling"])
        except:
            factor = 1
            
        # treat mask
        try:
            pass
            # TODO: that's wrong, use the mask in the callback
            # the mask must multiply the obtained value in hex or binary
            #address += math.log(int(point.find("Calculate").attrib["mask"]), 2)
        except:
            pass
        
        # Handle strings, not tested
        if format == "String":
            try:
                factor = float(address_el.attrib["multiple"])
            except KeyError:
                # One letter?
                factor = 1 # was already 1
                
        if table:
            create_mapping(template, address, label, table, factor, unit)
        else:
            msg = "Pass mapping %s %s %s %s %s %s" % (template, address, label, table, factor, unit)
            logger.warning(msg)
            unmapped.append(msg)
            print msg
    return unmapped

def create_all_templates_from_folder():
    suffix = ".xml"
    xml_paths = crawl(TEMPLATE_DIR, suffix)
    result = []
    for xml_path in xml_paths:
        xml_name = os.path.basename(xml_path)
        if xml_name.endswith(".xml"):
            xml_name = xml_name[:-4]
        print xml_name
        try:
            template = find_template_from_file_name(xml_name)
        except Template.DoesNotExist:
            template = Template(label=xml_name, file_name=xml_name)
            logger.info("Created new template %s" % template)
            template.save()
        result.extend(create_mappings_to_template_from_xml(template))
    return result
        
def create_all_documents_from_folder():
    suffix = ".xml"
    xml_paths = crawl(TEMPLATE_DIR, suffix)
    for xml_path in xml_paths:
        try:
            document = Document.objects.get(docfile=xml_path)
            logger.debug("Found doc %s for path %s" % (document, xml_path))
        except Document.DoesNotExist:
            new_doc = Document(docfile=xml_path)
            new_doc.save()
            logger.info("Created doc %s for path %s" % (new_doc, xml_path))

def main():
    logger.info("'templates' command called")
    create_all_documents_from_folder()
    unmapped_templates = create_all_templates_from_folder()
    return unmapped_templates

class Command(BaseCommand):
    help = "Creates all the necessary Template and AddressMapping objects from the files int the modbus_templates folder. Note that the template's name is generated from the file name (without .xml)"
    
    def handle(self, *args, **options):
        # make sure to call main, since a view will call the same
        main()
