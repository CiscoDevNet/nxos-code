#!/usr/bin/env python

from ncclient import manager
import sys

# Add parent directory to path to allow importing common vars
sys.path.append("..") # noqa
from device_info import sbx_n9kv_ao as device # noqa

# create a main() method
def main():
    """
    Main method that prints netconf capabilities of remote device.
    """
    with manager.connect(host = device["address"],
                         port = device["netconf_port"],
                         username = device["username"],
                         password = device["password"],
                         hostkey_verify = False) as m:


        # print all NETCONF capabilities
        print('\n***Remote Devices Capabilities for device {}***\n'.format(device["address"]))
        for capability in m.server_capabilities:
            print(capability.split('?')[0])


if __name__ == '__main__':
    sys.exit(main())
