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
    Main method that adds loopback interfaces and configures an IP address
    """

    add_ip_interface = """<config>
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <intf-items>
            <lb-items>
                <LbRtdIf-list>
                    <id>lo{id}</id>
                    <adminSt>up</adminSt>
                    <descr>Full intf config via NETCONF</descr>
                </LbRtdIf-list>
            </lb-items>
        </intf-items>
        <ipv4-items>
            <inst-items>
                <dom-items>
                    <Dom-list>
                        <name>default</name>
                        <if-items>
                            <If-list>
                                <id>lo{id}</id>
                                <addr-items>
                                    <Addr-list>
                                        <addr>{ip}</addr>
                                    </Addr-list>
                                </addr-items>
                            </If-list>
                        </if-items>
                    </Dom-list>
                </dom-items>
            </inst-items>
        </ipv4-items>
    </System>
    </config>""".format(id = loopback["id"], ip = loopback["ip"])
    print(add_ip_interface)

    with manager.connect(host = device["address"],
                         port = device["netconf_port"],
                         username = device["username"],
                         password = device["password"],
                         hostkey_verify = False) as m:

        # Add the loopback interface
        print("\nNow adding Looopback {} IP address {} to device {}...\n".format(loopback["id"], loopback["ip"], device["address"]))
        netconf_response = m.edit_config(target='running', config=add_ip_interface)
        # Parse the XML response
        print(netconf_response)


if __name__ == '__main__':
    sys.exit(main())
