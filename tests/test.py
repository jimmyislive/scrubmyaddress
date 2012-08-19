

from usps.address_info import Address, USPS

addr = Address('',
               '6406 Ivy Lane',  
               'Greenbelt', 
               'MD', 
               '', 
               '',
               None,
               0)

usps_connector = USPS([addr])
usps_connector.make_addr_std_request()

print usps_connector.output 
