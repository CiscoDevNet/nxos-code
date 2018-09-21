#!/usr/bin/env python

from ncclient import manager
import sys
from lxml import etree
import xmltodict

# Add parent directory to path to allow importing common vars
sys.path.append("..") # noqa
from device_info import sbx_n9kv_ao as device # noqa

# create a main() method
def main():
    """
    Main method that gets loopback interfaces 
    """

    get_oc_interface = """<filter>
    <interfaces xmlns="http://openconfig.net/yang/interfaces">
        <interface>
            <name/>
            <config>
                <type>ianaift:softwareLoopback</type>
            </config>
            <subinterfaces/>
        </interface>
    </interfaces>
    </filter>"""

    with manager.connect(host = device["address"],
                         port = device["netconf_port"],
                         username = device["username"],
                         password = device["password"],
                         hostkey_verify = False) as m:

        netconf_response = m.get_config('running', filter=get_oc_interface)

        loopbacks = xmltodict.parse(netconf_response.xml, force_list={"interface"})["rpc-reply"]["data"]["interfaces"]["interface"]

        print("The following loopbacks exist on the switch.")
        for loopback in loopbacks:
            try:
                print("  Loopback {} with IP {}".format(loopback["name"],
                                                        loopback["subinterfaces"]["subinterface"]["ipv4"]["addresses"]["address"]["config"]["ip"]))
            except KeyError:
                print("  Loopback {} with IP {}".format(loopback["name"],
                                                        "Not assigned"))

if __name__ == '__main__':
    sys.exit(main())
