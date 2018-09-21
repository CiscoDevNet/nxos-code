#!/usr/bin/env python

from ncclient import manager
import sys
from lxml import etree

# Add parent directory to path to allow importing common vars
sys.path.append("..") # noqa
from device_info import sbx_n9kv_ao as device # noqa

# Loopback Info - Change the details for your interface
loopback = {"id": "98", "ip": "10.98.98.1", "prefix": "24"}

# create a main() method
def main():
    """
    Main method that adds loopback interfaces
    """

    add_oc_interface = """<config>
    <interfaces xmlns="http://openconfig.net/yang/interfaces">
        <interface>
            <name>lo{id}</name>
            <config>
                <description> Configured using OpenConfig Model </description>
                <name>lo{id}</name>
                <type>ianaift:softwareLoopback</type>
            </config>
            <subinterfaces>
                <subinterface>
                    <index>0</index>
                    <ipv4>
                        <addresses>
                            <address>
                                <config>
                                    <ip>{ip}</ip>
                                    <prefix-length>{prefix}</prefix-length>
                                </config>
                                <ip>{ip}</ip>
                            </address>
                        </addresses>
                    </ipv4>
                </subinterface>
            </subinterfaces>
        </interface>
    </interfaces>
    </config>""".format(id = loopback["id"], ip = loopback["ip"], prefix = loopback["prefix"])

    # print(add_oc_interface)

    with manager.connect(host = device["address"],
                         port = device["netconf_port"],
                         username = device["username"],
                         password = device["password"],
                         hostkey_verify = False) as m:

        # Add the loopback interface IP
        print("\nNow adding IP address {} to interface lo{} on device {}...\n".format(loopback["ip"],
                                                                                      loopback["id"],
                                                                                      device["address"]))

        netconf_response = m.edit_config(target='running', config=add_oc_interface)
        # Parse the XML response
        print(netconf_response)

if __name__ == '__main__':
    sys.exit(main())
