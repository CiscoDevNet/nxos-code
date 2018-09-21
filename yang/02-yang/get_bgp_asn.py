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
    Main method that collects the ASN from the switch using the native model
    """

    asn_filter = """
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <bgp-items>
            <inst-items>
                <asn/>
            </inst-items>
        </bgp-items>
    </System>
    """

    with manager.connect(host = device["address"],
                         port = device["netconf_port"],
                         username = device["username"],
                         password = device["password"],
                         hostkey_verify = False) as m:

        # Add the loopback interface
        netconf_response = m.get(('subtree', asn_filter))
        # Parse the XML response
        xml_data = netconf_response.data_ele
        asn = xml_data.find(".//{http://cisco.com/ns/yang/cisco-nx-os-device}asn").text

        print("The ASN number for {} is {}".format(device["address"], asn))


if __name__ == '__main__':
    sys.exit(main())
