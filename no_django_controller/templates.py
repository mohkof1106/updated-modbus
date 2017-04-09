#!/usr/bin/env python
'''
Created on December 17, 2015
@author: victor
'''
import xml.etree.ElementTree as ET
import math

import os.path
BASE = os.path.dirname(__file__)

from objects import Device, Template, AddressMapping
from objects import get_link_format2table


### PROFILES ###
def get_anybus(slave_id, client):
    xml_name = "AnyBus Comunicator.xml"
    return get_device_by_name_and_id(xml_name, slave_id, client)
    
def get_device_by_name_and_id(xml_name, slave_id, client):
    "xml name as in the folder ex: AE 3TL Inverter (w/ or w/out .xml)"
    xml_path = os.path.join(BASE,"templates/") + xml_name
    if not xml_path.endswith(".xml"):
        xml_path += ".xml"
    template = create_template_from_xml(xml_path)
    return Device(template, slave_id, client)

### TEMPLATES ###
def create_template_from_xml(xml_path):
    """<Point id="1161514" name="02 -Length of model %2860 %3F%29">
         <Type>ShowValue</Type>
         <Address format="U16" index="40210" type="Holding"/>
         <Calculate/>
         <Enum/>
      </Point>
      <Point id="1161178" name="19 - Apparent Power" unit="VA">
         <Type>ShowValue</Type>
         <Address format="U16" index="40089" type="Holding"/>
         <Calculate scaling="0.1"/>
         <Enum/>"""
    link_format2table = get_link_format2table()
    tree = ET.parse(xml_path)
    root = tree.getroot()
    points, mappings = root.iter('Point'), []
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
            table = link_format2table[reg_type][table_format]()
        except:
            # TODO: what default?
            print label, address_el.attrib
            continue
        try:
            factor = float(point.find("Calculate").attrib["scaling"])
        except:
            factor = 1
        try:
            address += math.log(int(point.find("Calculate").attrib["mask"]), 2)
        except:
            pass
        mappings.append(AddressMapping(address, label, table, factor, unit))
    if mappings == []:
        return None
    return Template(mappings)

def print_unmappables():
    from tools import crawl
    template_dir, suffix = os.path.join(BASE,"templates"), ".xml"
    xml_paths = crawl(template_dir, suffix)
    for xml_path in xml_paths:
        create_template_from_xml(xml_path)

if __name__ == "__main__":
    print_unmappables()

    template = create_template_from_xml(os.path.join(BASE,"templates/AGC-4 Enerwhere Custom.xml"))
    print template.get_addresses()