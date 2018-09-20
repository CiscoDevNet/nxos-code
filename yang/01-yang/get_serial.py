#!/usr/bin/env python

from ncclient import manager
import sys
from lxml import etree

# Add parent directory to path to allow importing common vars
sys.path.append("..") # noqa
from device_info import sbx_n9kv_ao as device # noqa

# create a main() method
def main():
    """
    Main method that prints netconf capabilities of remote device.
    """
    serial_number = """
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <serial/>
    </System>
    """

    with manager.connect(host = device["address"],
                         port = device["netconf_port"],
                         username = device["username"],
                         password = device["password"],
                         hostkey_verify = False) as m:

        # Collect the NETCONF response
        netconf_response = m.get(('subtree', serial_number))
        # Parse the XML and print the data
        xml_data = netconf_response.data_ele
        serial =  xml_data.find(".//{http://cisco.com/ns/yang/cisco-nx-os-device}serial").text

        print("The serial number for {} is {}".format(device["address"], serial))

if __name__ == '__main__':
    sys.exit(main())
