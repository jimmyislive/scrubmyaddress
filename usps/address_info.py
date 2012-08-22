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
        
    def _parse_address(self, child, field):
        try:
            return str(child.find(field).text)
        except AttributeError:
            return ''
        
    def _make_base_request(self, tag, tags_to_ignore=[]):
        
        if tag == 'AddressValidateRequest':
            api = 'Verify'
        elif tag == 'ZipCodeLookupRequest':
            api = 'ZipCodeLookup'
        elif tag == 'CityStateLookupRequest':
            api = 'CityStateLookup'
            
        xml_data = ''
        for k,v in self.contents.items():
            xml_data += v.create_xml(tags_to_ignore)
            
        final_xml_data = '<%s USERID="%s">%s</%s>' % (tag, settings.USPS_USERNAME, xml_data, tag)
        
        url = 'http://%s/%s?API=%s&XML=%s' % (settings.PRODUCTION_SERVERNAME, settings.PRODUCTION_DLL, api,
                                                                   urllib.quote(final_xml_data))
        response = urllib.urlopen(url).read()
        
        root = et.fromstring(response)
        
        for address_child in root:
            id = address_child.attrib['ID']
            
            error_child = address_child.find('Error')
            if error_child: 
                self.contents[id].error = True
                self.contents[id].error_number = self._parse_address(error_child, 'Number')
                self.contents[id].error_source = self._parse_address(error_child, 'Source')
                self.contents[id].error_description = self._parse_address(error_child, 'Description')
                print 'An error has occurred: number: %s, source: %s, description: %s' % \
                                        (self.contents[id].error_number, self.contents[id].error_source, self.contents[id].error_description)
            else:
                self.contents[id].standardized_firm_name = self._parse_address(address_child, 'FirmName')
                self.contents[id].standardized_address_line1 = self._parse_address(address_child, 'Address1')
                self.contents[id].standardized_address_line2 = self._parse_address(address_child, 'Address2')
                self.contents[id].standardized_city = self._parse_address(address_child, 'City')
                self.contents[id].standardized_state = self._parse_address(address_child, 'State')
                self.contents[id].standardized_zip5 = self._parse_address(address_child, 'Zip5')
                self.contents[id].standardized_zip4 = self._parse_address(address_child, 'Zip4')
                
    def make_addr_std_request(self):
        self._make_base_request('AddressValidateRequest')
        
    def make_zip_code_lookup_request(self):
        self._make_base_request('ZipCodeLookupRequest', ['Urbanization',
                                                         'Zip5', 'Zip4'])
        
    def make_city_state_lookup_request(self):
        self._make_base_request('CityStateLookupRequest', ['FirmName', 'Address1', 'Address2', 'City', 'State', 'Urbanization', 'Zip4'])
        
class Address(object):
    ''''''
    
    def __init__(self, firm_name, address_line1, address_line2, city, state, 
                 zip5, zip4=None, urbanization=None, id=None):
        self.firm_name = firm_name
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
        
        self.standardized_firm_name = ''
        self.standardized_address_line1 = ''
        self.standardized_address_line2 = ''
        self.standardized_city = ''
        self.standardized_state = ''
        self.standardized_urbanization = ''
        self.standardized_zip5 = ''
        self.standardized_zip4 = ''
        
        self.error = False
        self.error_number = '' 
        self.error_source = ''
        self.error_description = '' 

    def create_xml(self, tags_to_ignore=[]):

        if 'Address1' in tags_to_ignore and 'Address2' in tags_to_ignore:
            root = et.Element('ZipCode', {'ID': self.id})
        else:
            root = et.Element('Address', {'ID': self.id})
            
        if 'FirmName' not in tags_to_ignore:
            firm_name_ele = et.SubElement(root, 'FirmName')
            firm_name_ele.text = self.firm_name
        if 'Address1' not in tags_to_ignore:
            address_line1_ele = et.SubElement(root, 'Address1')
            address_line1_ele.text = self.address_line1
        if 'Address2' not in tags_to_ignore:
            address_line2_ele = et.SubElement(root, 'Address2')
            address_line2_ele.text = self.address_line2
        if 'City' not in tags_to_ignore:
            city_ele = et.SubElement(root, 'City')
            city_ele.text = self.city
        if 'State' not in tags_to_ignore:
            state_ele = et.SubElement(root, 'State')
            state_ele.text = self.state
        #optional, only for PR
        if 'Urbanization' not in tags_to_ignore:
            if self.state == 'PR' and self.urbanization:
                urbanization_ele = et.SubElement(root, 'Urbanization')
                urbanization_ele.txt = self.urbanization
        if 'Zip5' not in tags_to_ignore:
            zip5 = et.SubElement(root, 'Zip5')
            zip5.text = str(self.zip5)
        if 'Zip4' not in tags_to_ignore:
            zip4 = et.SubElement(root, 'Zip4')
            zip4.text = str(self.zip4)
        
        return et.tostring(root)
    

