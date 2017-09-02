#!/bin/bash

HOSTS='/etc/hosts'
NETWORK='/etc/sysconfig/network'
IFCFG='/etc/sysconfig/network-scripts/ifcfg-bond0'

[ $# -ne 1 ] && echo "Usage: sh $0 new_ip" && exit

old_ip=`ifconfig bond0|grep "\baddr"|awk -F: '{print $2}'|cut -d ' ' -f 1`
old_hostname=${old_ip//./-}
new_ip=$1
new_hostname=${new_ip//./-}

echo "--- --- --- --- ---"
echo $NETWORK
echo "--- --- --- --- ---"
sed -i "s/$old_hostname/$new_hostname/" $NETWORK
echo "--- --- --- --- ---"
echo $IFCFG
echo "--- --- --- --- ---"
sed -i "s/$old_ip$/$new_ip/;s/${old_ip%.*}/${new_ip%.*}/" $IFCFG
echo "--- --- --- --- ---"
echo $HOSTS
echo "--- --- --- --- ---"
sed -i "s/$old_hostname/$new_hostname/g" $HOSTS
