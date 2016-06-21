#! /bin/bash
#表名用空格分开，$1$2为时间范围，默认导出整表
tables=(page_info page_module_info)
hdfs_tmp_path="tmp_export"

USER=hadoop
HBASE_CMD=/home/$USER/hbase/bin/hbase
HADOOP_CMD=/home/$USER/hadoop/bin/hadoop

${HADOOP_CMD} fs -rm -r /${hdfs_tmp_path}

for table in ${tables[@]}
do
    if [ ! -n "$1" ]; then   
       echo "full export...."
       /sbin/runuser -l ${USER} -c "/home/${USER}/hbase/bin/hbase org.apache.hadoop.hbase.mapreduce.Export ${table} /${hdfs_tmp_path}/${table}"
    elif [ ! -n "$2" ]; then
       echo "export from {$1} to now...."
       startTime=`date -d "$1" +%s`000
       echo startTime '>>>' $startTime
       /sbin/runuser -l ${USER} -c "/home/${USER}/hbase/bin/hbase org.apache.hadoop.hbase.mapreduce.Export ${table} /${hdfs_tmp_path}/${table} 1 ${startTime}"
    else 
       echo "export from {$1} to ${2}...."
       startTime=`date -d "$1" +%s`000
       endTime=`date -d "$2" +%s`000
       /sbin/runuser -l ${USER} -c "/home/${USER}/hbase/bin/hbase org.apache.hadoop.hbase.mapreduce.Export ${table} /${hdfs_tmp_path}/${table} 1 ${startTime} ${endTime}"
    fi
done

cd /home/${USER}/

if [  -d "${hdfs_tmp_path}" ]; then
   rm -rf ${hdfs_tmp_path}
fi

/sbin/runuser -l ${USER} -c "${HADOOP_CMD} fs -copyToLocal /${hdfs_tmp_path} ."  
tar acf tmp_export.tar.gz tmp_export

scp tmp_export.tar.gz root@172.16.7.101@:/home/smb/public/tmp/
#scp -P 58000 tmp_export.tar.gz root@182.150.21.99:/home/smb/public/tmp/
