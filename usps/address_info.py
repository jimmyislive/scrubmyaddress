#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import urllib
import xml.etree.cElementTree as et

from scrubmyaddress import settings

class USPS(object):
    
    def __init__(self, obj_list):
        self.contents = {}
        for obj in obj_list:
            self.contents[obj.id] = obj
        
        #self.output = {}
        
    def _parse_address(self, address_child, field):
        try:
            return str(address_child.find(field).text)
        except AttributeError:
            return ''
        
    def make_addr_std_request(self):
        xml_data = ''
        for k,v in self.contents.items():
            xml_data += v.create_xml()
            
        final_xml_data = '<AddressValidateRequest USERID="%s">%s</AddressValidateRequest>' % (settings.USPS_USERNAME,
                                                                                              xml_data)
        url = 'http://%s/ShippingAPITest.dll?API=Verify&XML=%s' % (settings.TESTING_SERVERNAME,
                                                                   urllib.quote(final_xml_data))
        
        response = urllib.urlopen(url).read()
        
        root = et.fromstring(response)
        
        if root.tag == 'AddressValidateResponse':
            #everything is ok
            for address_child in root:
                id = address_child.attrib['ID']
                self.contents[id].standardized_address_line1 = self._parse_address(address_child, 'Address1')
                self.contents[id].standardized_address_line2 = self._parse_address(address_child, 'Address2')
                self.contents[id].standardized_city = self._parse_address(address_child, 'City')
                self.contents[id].standardized_state = self._parse_address(address_child, 'State')
                self.contents[id].standardized_zip5 = self._parse_address(address_child, 'Zip5')
                self.contents[id].standardized_zip4 = self._parse_address(address_child, 'Zip4')
        
class Address(object):
    ''''''
    
    def __init__(self, address_line1, address_line2, city, state, 
                 zip5, zip4=None, urbanization=None, id=None):
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.city = city
        self.state = state
        self.urbanization = urbanization
        self.zip5 = zip5
        self.zip4 = zip4
        if id:
            self.id = id
        else:
            self.id = '%s-%s' % (time.time(), random.randint(1, 100000))
        
        self.standardized_address_line1 = ''
        self.standardized_address_line2 = ''
        self.standardized_city = ''
        self.standardized_state = ''
        self.standardized_urbanization = ''
        self.standardized_zip5 = ''
        self.standardized_zip4 = ''

    def create_xml(self):
        #address_ele = et.SubElement(root, 'Address', {'ID': self.id})
        root = et.Element('Address', {'ID': self.id})
        address_line1_ele = et.SubElement(root, 'Address1')
        address_line1_ele.text = self.address_line1
        address_line2_ele = et.SubElement(root, 'Address2')
        address_line2_ele.text = self.address_line2
        city_ele = et.SubElement(root, 'City')
        city_ele.text = self.city
        state_ele = et.SubElement(root, 'State')
        state_ele.text = self.state
        #optional, only for PR
        if self.state == 'PR' and self.urbanization:
            urbanization_ele = et.SubElement(root, 'Urbanization')
            urbanization_ele.txt = self.urbanization
        zip5 = et.SubElement(root, 'Zip5')
        zip5.text = str(self.zip5)
        zip4 = et.SubElement(root, 'Zip4')
        zip4.text = str(self.zip4)
        
        return et.tostring(root)
    

