#!/usr/bin/env python

from ncclient import manager
import sys
import xmltodict
from pprint import pprint

# Add parent directory to path to allow importing common vars
sys.path.append("..") # noqa
from device_info import sbx_n9kv_ao as device # noqa

# create a main() method
def main():
    """
    Main method that retrieves and prints loopback interfaces on the device.
    """
    loopback_filter = """
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <intf-items>
            <lb-items/>
        </intf-items>
    </System>
    """
    ip_interface_filter = """
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <ipv4-items>
        <inst-items>
            <dom-items>
                <Dom-list>
                    <name>default</name>
                    <if-items>
                        <If-list/>
                    </if-items>
                </Dom-list>
            </dom-items>
        </inst-items>
    </ipv4-items>
    </System>
    """

    with manager.connect(host = device["address"],
                         port = device["netconf_port"],
                         username = device["username"],
                         password = device["password"],
                         hostkey_verify = False) as m:

        # Collect the NETCONF response
        loopback_response = m.get(('subtree', loopback_filter))
        ip_interface_response = m.get(('subtree', ip_interface_filter))

        # Convert reply into Python Dictionary
        loopbacks = xmltodict.parse(loopback_response.xml, force_list={"LbRtdIf-list"})["rpc-reply"]["data"]["System"]["intf-items"]["lb-items"]["LbRtdIf-list"]
        ip_interfaces = xmltodict.parse(ip_interface_response.xml, force_list={"If-list", "Addr-list"})["rpc-reply"]["data"]["System"]["ipv4-items"]["inst-items"]["dom-items"]["Dom-list"]["if-items"]["If-list"]
        print("The following loopbacks exist on the switch.")
        for loopback in loopbacks:
            print("  Loopback {}".format(loopback["id"]))
        print("The following loopbacks have IP addresses assigned.")
        for interface in ip_interfaces:
            if interface["id"][:2] == "lo":
                print("  Loopback {} with IP {}".format(interface["id"], interface["addr-items"]["Addr-list"][0]["addr"]))


if __name__ == '__main__':
    sys.exit(main())
