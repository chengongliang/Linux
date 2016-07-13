#!/bin/bash
source /etc/profile 2>&1>/dev/null
if [[ `pwd` != "/home/webuser" ]];then
    echo -e "\033[35mPlease run this script in /home/webuser\033[0m"
    exit
fi
file=`find . -type f -name '*.properties'|xargs grep -lE '^metadata|^zookeeper'`
echo -e "$file\n"
echo -e "$file\n" > webuser.tmp
read -p "Please enter (y/yes) to confirm: " enter
if [[ $enter = "y" || $enter = "yes" ]];then
    for f in $file;do
        sed -i "/#metadata/{/#metadata/d}" $f
        sed -i "/metadata/a\metadata.broker.list=mysql3:9092,worker1:9092" $f
        sed -i "0,/metadata/{/metadata/d}" $f
        sed -i "/#zookeeper/{/#zookeeper/d}" $f
        sed -i "/zookeeper/a\zookeeper.connect=192.168.100.31:2181,192.168.100.32:2181,192.168.100.4:2181" $f
        sed -i "0,/zookeeper/{/zookeeper/d}" $f
    done
    webuser=`awk -F'/' '{print $2}' webuser.tmp|uniq`
    for i in $webuser;do
        echo -e "\033[32mNow restart $i\033[0m"
        PID=$(jps -v|grep -v grep|grep $i|awk '{print $1}')
        kill -9 $PID
        bash $i/bin/startup.sh
    done
fi
