#!/bin/bash

date=`date +%F`
Time=`date +%H:%M`
back_dir=/data/db_back/${date}/${Time}
user=root
passwd=password

db_list=`/alidata/server/mysql/bin/mysql -u${user} -p${passwd} -e "show databases;" |grep -Evi "database|performance|information|mysql"`

[ -d ${back_dir} ] || mkdir -p ${back_dir}
for dbname in ${db_list};
do
    /alidata/server/mysql/bin/mysqldump -u${user} -p${passwd} --single-transaction -B ${dbname} > ${back_dir}/${dbname}.sql 
done
cd /data/db_back
if [[ $(pwd) == "/data/db_back" ]];then
    find . -type d -name "2016*" -mtime +30 | xargs rm -rf
fi
