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
    Main method that adds an IP address to interface loopback
    """

    loopback_ip_add = """
    <config>
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <ipv4-items>
        <inst-items>
            <dom-items>
                <Dom-list>
                    <name>default</name>
                    <if-items>
                        <If-list>
                            <id>lo{}</id>
                            <addr-items>
                                <Addr-list>
                                    <addr>{}</addr>
                                </Addr-list>
                            </addr-items>
                        </If-list>
                    </if-items>
                </Dom-list>
            </dom-items>
        </inst-items>
    </ipv4-items>
    </System>
    </config>""".format(loopback["id"], loopback["ip"])

    with manager.connect(host = device["address"],
                         port = device["netconf_port"],
                         username = device["username"],
                         password = device["password"],
                         hostkey_verify = False) as m:

        # Add the loopback interface
        print("\nNow adding Looopback {} IP address {} to device {}...\n".format(loopback["id"], loopback["ip"], device["address"]))
        netconf_response = m.edit_config(target='running', config=loopback_ip_add)
        # Parse the XML response
        print(netconf_response)

if __name__ == '__main__':
    sys.exit(main())
