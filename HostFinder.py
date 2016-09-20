#!/usr/bin/env

import sys, getopt, logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) #suppress scapy warning message
from scapy.all import *

interface = "eth0"
scannableIP = "192.168.0.0"
scannableCIDR = "16"
helpSection = ("HostFinder - Active ARP Ping Scan Tool\n"
			   "Written By : Fatih KAYRAN <kayranfatih@hotmail.com>\n\n" 
			   "Usage Hostfinder [-i interface] [-r range ]\n"
			   "-i interface : The interface in use\n"
			   "-r range : scannable IP and CIDR(eg:192.168.1.0/24).\n"
			   "If there are no options to scan, HostFinder will use these argument.\n"
			   "inteface : eth0\n"
			   "range : 192.168.0.0/16\n")


def GetArgument():
	options, remainder = getopt.getopt(sys.argv[1:], 'i:r:h')
	for opt, arg in options:
		if opt in ('-i'):
			global interface 
			interface = arg			
		elif opt in ('-r'):
			global scannableIP
			global scannableCIDR
			scannableIP = arg.split('/')[0]
			scannableCIDR = arg.split('/')[1]
		elif opt in ('-h'):
			print helpSection
			exit(0)

if __name__ == '__main__': 

	GetArgument()

	try :

		ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=scannableIP + "/" + scannableCIDR), timeout=3, iface=interface, verbose=0)

		print "-"*41 + "\nInterface : " + interface + " " + "Range : " +scannableIP + "/" + scannableCIDR + "\n" + "-"*41
		print " "*3 + "Mac Adress" + " "*6 + "IP Adress\n"

		for s, r in ans : 
			print r.sprintf("%Ether.src% %ARP.psrc%")

	except socket.error :
		print "Invalid interface / IP"

	except ValueError :
		print "Invalid IP/CIDR format (e.g 192.168.1.0/24)"