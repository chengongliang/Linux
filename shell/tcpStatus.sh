#!/bin/bash

logfile=/home/tcpstatus.log

if [ -f $logfile ];then
    touch $logfile
fi
echo "--------------------`date +%F/%k:%M:%S`-------------------" >> $logfile
netstat -n | grep :80|awk '/^tcp/{print $5}'|cut -d ":" -f1|sort |uniq -c|sort -nr|head -n5 >> $logfile
netstat -n | grep :80|awk '/^tcp/{++S[$NF]}END{for (i in S) print i,S[i]}' >> $logfile
