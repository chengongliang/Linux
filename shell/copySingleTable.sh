#! /bin/bash
# 集群间 单表拷贝脚本
# 输入参数：<表名> <目标集群zookeeper地址>

#DATE=`date +%Y-%m-%d`
HBASE_CMD=/home/x_hdfs/hbase/bin/hbase

if [ -z $1 ]; then
  echo "please passing table to be sync"
  exit
fi
if [ -z $2 ]; then
  echo "please passing remote hbase zookeeper addr"
  exit
fi

table=$1
PEER=$2

$HBASE_CMD org.apache.hadoop.hbase.mapreduce.CopyTable --peer.adr=$PEER:2181:/hbase $table
