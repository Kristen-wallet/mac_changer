#!/usr/bin/env python3
import subprocess as sub
import optparse as opt
import re

def get_argument():
    parser = opt.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="MAC address Assign")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-]Please specify an Interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-]Please specify MAC address, use --help for more info.")
    return options

def mac_changer(interface, new_mac):
    print("[+]Changing MAC address for ", interface, " to ", new_mac)
    sub.call(["ifconfig", interface, "down"])
    sub.call(["ifconfig", interface, "hw", "ether", new_mac])
    sub.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    interface_result = sub.check_output(["ifconfig", interface])
    mac_search_result=re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(interface_result))
    if mac_search_result:
        return mac_search_result.group(0)
    else:
        print("[-]Could not read MAC Address.")

options = get_argument()
current_mac = get_current_mac(options.interface)
print("Current MAC: ",current_mac)
mac_changer(options.interface,options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+]MAC Address was successfully changed to ",current_mac)
else:
    print("[-]MAC Address did not get changed")