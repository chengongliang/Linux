#! /bin/bash
#tables=(student_license_pen_data)
tables=(resource_manager resource_manager_indexing)
hdfs_tmp_path="/tmp_export/"

USER=hadoop
HBASE_CMD=/home/$USER/hbase/bin/hbase
HADOOP_CMD=/home/$USER/hadoop/bin/hadoop

cd /home/$USER
scp root@172.16.7.101:/home/smb/public/tmp/tmp_export.tar.gz .
tar axf tmp_export.tar.gz

${HADOOP_CMD} fs -rm -r ${hdfs_tmp_path}
${HADOOP_CMD} fs -copyFromLocal tmp_export /

for table in ${tables[@]}
do
   ${HBASE_CMD} org.apache.hadoop.hbase.mapreduce.Import ${table} ${hdfs_tmp_path}${table}
done
