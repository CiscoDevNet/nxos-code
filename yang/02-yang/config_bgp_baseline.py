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
    Main method that ensures baseline BGP configuration present on device.
    """
    with open("bgp-baseline.xml") as f:
        bgpconfig = f.read()

    # print(bgpconfig)

    with manager.connect(host = device["address"],
                         port = device["netconf_port"],
                         username = device["username"],
                         password = device["password"],
                         hostkey_verify = False) as m:

        # Add the loopback interface
        print("\nNow sending baseline bgp configuration to device {}...\n".format(device["address"]))
        netconf_response = m.edit_config(target='running', config=bgpconfig)
        # Parse the XML response
        print(netconf_response)


if __name__ == '__main__':
    sys.exit(main())
