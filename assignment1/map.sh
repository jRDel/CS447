#!/bin/bash

output=$(ip -brief link show dev "$1" | tr -s " ") #$1 is the name of the interface, IE: eth1
#ip -brief command will give us the name of the interface

eval $(echo $output | awk '{print "iface="$1} ' ) #Create two vars iface and iface_mac and populate them

iface_bus=$(ethtool -i $iface | awk '/0000:/ {print $2}')


#map arg1 arg2
#arg1 and arg2 are fed into this script as stdin so you have to read them with read(2).

while read bus name; do

	if [ "${iface_bus}" = "${bus}" ]; then
		#if the interface bus matches the bus passed in as an argument.
		#The first value sent to stdout should be logical configuration that
		# the physical interface should use
		echo $name
	fi
done

exit 0
