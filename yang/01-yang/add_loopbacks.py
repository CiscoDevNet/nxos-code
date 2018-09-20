#!/usr/bin/env python

from ncclient import manager
import sys
from lxml import etree

# Add parent directory to path to allow importing common vars
sys.path.append("..") # noqa
from device_info import sbx_n9kv_ao as device # noqa

# Loopback Info - Change the details for your interface
loopback = {"id": "99", "ip": "10.99.99.1/24"}

# create a main() method
def main():
    """
    Main method that adds loopback interface 
    """
    loopback_add = """
    <config>
        <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
            <intf-items>
                <lb-items>
                    <LbRtdIf-list>
                        <id>lo{}</id>
                        <adminSt>up</adminSt>
                        <descr>Interface added via NETCONF</descr>
                    </LbRtdIf-list>
                </lb-items>
            </intf-items>
        </System>
    </config>""".format(loopback["id"])

    with manager.connect(host = device["address"],
                         port = device["netconf_port"],
                         username = device["username"],
                         password = device["password"],
                         hostkey_verify = False) as m:

        # Add the loopback interface
        print("\nNow adding Loopback{} device {}...\n".format(loopback["id"], device["address"]))
        netconf_response = m.edit_config(target='running', config=loopback_add)
        # Parse the XML response
        print(netconf_response)

if __name__ == '__main__':
    sys.exit(main())
