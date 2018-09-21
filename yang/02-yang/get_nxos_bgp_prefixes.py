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
    Main method that collects the BGP prefixes
    """
    filter_prefix = """<filter>
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <bgp-items>
            <inst-items>
                <dom-items>
                    <Dom-list>
                        <name>default</name>
                        <af-items>
                            <DomAf-list>
                                <type>ipv4-ucast</type>
                                <prefix-items>
                                    <AdvPrefix-list/>
                                </prefix-items>
                            </DomAf-list>
                        </af-items>
                    </Dom-list>
                </dom-items>
            </inst-items>
        </bgp-items>
    </System>
    </filter>"""

    with manager.connect(host = device["address"],
                         port = device["netconf_port"],
                         username = device["username"],
                         password = device["password"],
                         hostkey_verify = False) as m:

        # Add the prefix to BGP
        print("\nNow getting configured prefixes on device {}..\n".format(device["address"]))
        netconf_response = m.get_config('running', filter=filter_prefix)

        # Convert reply into Python Dictionary
        prefixes = xmltodict.parse(netconf_response.xml, force_list={"AdvPrefix-list"})["rpc-reply"]["data"]["System"]["bgp-items"]["inst-items"]["dom-items"]["Dom-list"]["af-items"]["DomAf-list"]["prefix-items"]["AdvPrefix-list"]
        print("The following prefixes are configured in bgp on the switch.")
        for prefix in prefixes:
            print("  - {}".format(prefix["addr"]))

        # Parse the XML response
        # print(netconf_response)

if __name__ == '__main__':
    sys.exit(main())
