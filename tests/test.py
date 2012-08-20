

from usps.address_info import Address, USPS

'''
addr = Address('',#firm name
               '', #address line1
               '6406 Ivy Lane', #address line2  
               'Greenbelt', #city
               'MD', #state
               '', 
               '',
               None,
               0)

usps_connector = USPS([addr])


usps_connector.make_addr_std_request()

print addr.standardized_address_line1
print addr.standardized_address_line2
print addr.standardized_city
print addr.standardized_state
print addr.standardized_zip5
print addr.standardized_zip4 


usps_connector.make_zip_code_lookup_request()

print addr.standardized_address_line1
print addr.standardized_address_line2
print addr.standardized_city
print addr.standardized_state
print addr.standardized_zip5
print addr.standardized_zip4 
'''

addr = Address('',#firm name
               '', #address line1
               '', #address line2  
               '', #city
               '', #state
               '90210', 
               '',
               None,
               0)

usps_connector = USPS([addr])
usps_connector.make_city_state_lookup_request()

print addr.standardized_address_line1
print addr.standardized_address_line2
print addr.standardized_city
print addr.standardized_state
print addr.standardized_zip5
print addr.standardized_zip4 




