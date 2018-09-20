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
    Main method that removes loopback interface
    """
    loopback_remove = """
    <config>
        <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
            <intf-items>
                <lb-items>
                    <LbRtdIf-list operation="remove">
                        <id>lo{id}</id>
                    </LbRtdIf-list>
                </lb-items>
            </intf-items>
        </System>
    </config>""".format(id = loopback["id"], ip = loopback["ip"])

    with manager.connect(host = device["address"],
                         port = device["netconf_port"],
                         username = device["username"],
                         password = device["password"],
                         hostkey_verify = False) as m:

        # Add the loopback interface
        print("\nNow removing Loopback{} from device {}...\n".format(loopback["id"], device["address"]))
        netconf_response = m.edit_config(target='running', config=loopback_remove)
        # Parse the XML response
        print(netconf_response)

if __name__ == '__main__':
    sys.exit(main())
