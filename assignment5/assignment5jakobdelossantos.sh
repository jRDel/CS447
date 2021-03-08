#!/bin/bash


options=$(getopt -o b: -- "$@")

[ $? -eq 0 ] || {
    echo "Incorrect options provided"
    exit 1
}

eval set -- "$options"

blockdevs=()

while true; do
    case "$1" in
    -b)
	# TODO: Append to array blockdevs
	blockdevs+=("$2")	
        ;;

    --)
        shift
        break
        ;;
    esac
    shift
done

echo "Array Size: ${#blockdevs[@]}"

#I commented out the following TODO because if you pass it two block devices, which we are in our case, it will just exit
#TODO
#Test if blockdevs array has two elements.
#If echo an error message and exit with a non-zero
# exit code.

#if [ "${#blockdevs[@]}" == 2 ]; then
#	echo "Array size is 2. Exiting..."
#	exit 2
#fi

#TODO
#Test to see if /dev/md/0 exists.
#If it exists stop the array with mdadm.
#If it does not exist echo "/dev/md/0" does
#not exist

if [ -d "/dev/md/0" ]
then
	mdadm --stop /dev/md/0
else
	echo "/dev/md/0 does not exist."
fi

#TODO
#Loop over elements in blockdevs and
# dd test.raw to each block device

for element in "${blockdevs[@]}"
do
	dd if=/tmp/test.raw of=${element}
done

#TODO
#Loop over each the elements in blockdevs and
#create a GPT partition table and create one partition
# from 1MB to 1024MB

for element in "${blockdevs[@]}"
do
	parted ${element} --script mklabel gpt
	parted ${element} --script mkpart primary ext4 1MiB 1025MiB
done	

#TODO
#Create a RAID-1 named "0" with the partitions created by the previous command(s)
mdadm --create 0 --level 1 --raid-devices 2 /dev/vdb1 /dev/vdc1


exit 0
