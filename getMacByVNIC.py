#!/usr/bin/env python2
"""Fetches a MAC address of a particular vNIC from a UCSM SP.
"""

from __future__ import print_function
import argparse
from ucsmsdk.ucshandle import UcsHandle

def parse_args():
    """Read arguments from command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ucsip",
        help="IP address or hostname of UCSM",
        required=True
        )
    parser.add_argument(
        "--ucsuser",
        help="username to use for UCSM connection",
        required=True
        )
    parser.add_argument(
        "--ucspass",
        help="password to use for UCSM connection",
        required=True
        )
    parser.add_argument(
        "--spname",
        help="UCS Service Profile Name",
        required=True
        )
    parser.add_argument(
        "--vnicname",
        help="UCS vNIC Name",
        required=True
        )

    myargs = parser.parse_args()

    return myargs

def sp_macaddress(handle, sp_name, parent_dn="org-root"):
    """
    This function will return the mac addresses of a service profile
    Args:
        handle (UcsHandle)
        sp_name (string): Service Profile  name.
        parent_dn (string): Org.
    Returns:
        dict containing:
        adaptor name
        mac address
    Raises:
        ValueError: If LsServer is not present
    Example:
        sp_macaddress(handle, sp_name="sample_sp",
                      parent_dn="org-root")
        sp_macaddress(handle, sp_name="sample_sp",
                      parent_dn="org-root/sub-org")
    """
    dn = parent_dn + "/ls-" + sp_name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("sp '%s' does not exist" % dn)

    mac_dict = {}

    query_data = handle.query_children(in_mo=mo, class_id='VnicEther')
    for item in query_data:
        mac_dict[item.name] = item.addr

    return mac_dict

def get_vnic_mac_from_sp(ipaddr, user, pword, sp_name, vnic_name):
    """get mac of vnic from service profile."""
    handle = UcsHandle(ipaddr, user, pword)
    handle.login()
    macs = sp_macaddress(handle, sp_name)
    handle.logout()
    my_output = macs[vnic_name]
    return my_output

if __name__ == '__main__':

    ARGS = parse_args()
    OUTPUT = get_vnic_mac_from_sp(
        ARGS.ucsip, ARGS.ucsuser, ARGS.ucspass, ARGS.spname, ARGS.vnicname)
    if OUTPUT is not None:
        print(OUTPUT)
        exit(0)
    else:
        print("ERROR: no mac address found for ", ARGS.vnicname)
        exit(1)
