#! /usr/bin/python

import time
import datetime
from datetime import date
import sys
import os

# 取hbase 所有表名
output=os.popen("echo 'list' | /home/hadoop/hbase/bin/hbase shell | grep '\[.*\]'").read()
tables=output[1:len(output)-2].replace('"','').replace(' ','').split(',')

# 需过滤的表
filters=["tsinghua_edu_history_exsite","tsinghua_edu_history_word","tsinghua_edu_standart_exsite","tsinghua_edu_standart_word","resource_manager_indexing","tsinghua_edu_context_index"]
tables=[i for i in tables if i not in filters]

today=date.today()

#os.system("scp -P 58002 root@182.150.*.*:/home/hadoop4test/lastImportDat1111e /home/hadoop/")

RemoteServer69  = os.system("ssh -p 55556 root@182.150.*.** pwd")

# 最近一次同步的日期
f = open('/root/lastImportDate','r')
lastImportDate = datetime.datetime.strptime(f.readline().strip(), "%Y-%m-%d %H:%M:%S,%f")
f.close()
yesterday=datetime.date.today() - datetime.timedelta(days=1)
lastImportDateStamp = time.mktime(lastImportDate.timetuple())

tarFile="increment." + yesterday.isoformat() + ".tar.gz"

if RemoteServer69 == 0:
  backupDst="/hbase_dump"
  os.system("source /home/hadoop/.bashrc")
  synTables='/home/hadoop/synTables'
  createTables='/home/hadoop/createTables'
  file=open(synTables,'w')
  files=open(createTables, 'w')
  for tablename in tables:
    LZCMD="echo \"describe \'%s\'\" | /home/hadoop/hbase/bin/hbase shell | awk -F\"NAME => \" '{print $2}' | awk -F\",\" '{print $1}'" %(tablename)
    liezu1 = os.popen(LZCMD).read()
    liezu2 = liezu1[1:len(liezu1)-2].replace('\n','')
    GetR="'%s', %s" %(tablename, liezu2)
    files.write(GetR)
    files.write("\n")
    file.write(tablename)
    file.write("\n")
    # 每月16号全量同步
    if today.day == 16:
      backupSubFolder=backupDst + "/full/" + yesterday.isoformat() + "/" + tablename
      cmd="/sbin/runuser -l hadoop -c '/home/hadoop/hbase/bin/hbase org.apache.hadoop.hbase.mapreduce.Export %s %s'"%(tablename, backupSubFolder)
      os.system(cmd)
    # 增量同步
    backupSubFolder=backupDst+"/increment/"+yesterday.isoformat()+"/"+tablename
    cmd="/sbin/runuser -l hadoop -c '/home/hadoop/hbase/bin/hbase org.apache.hadoop.hbase.mapreduce.Export %s %s 1 %s'"%(tablename,backupSubFolder,str(int(lastImportDateStamp)*1000))
    os.system(cmd)

  file.close()
  files.close()
  # 导出的数据拷贝到本地
  copyCmd="/sbin/runuser -l hadoop -c '/home/hadoop/hadoop/bin/hdfs dfs -copyToLocal " + backupDst + "/increment/" + yesterday.isoformat() + " /home/hadoop/increment_dump/'"
  os.system(copyCmd)
  os.system("mv /home/hadoop/increment_dump/" + yesterday.isoformat() + " /root/increment/")
  os.system("tar czf " + tarFile + " increment/" + yesterday.isoformat())
  os.system("scp -P 55556 " + synTables + " root@182.150.*.*:/data/hecran/hbase/")
  os.system("scp -P 55556 " + createTables + " root@182.150.*.*:/data/hecran/hbase/")
else:
  os.system("echo \"RemoteServer [172.16.6.10] is down\" | /bin/mailx -s \"Hbase_dump OnLine ERROR\" biqin@tsinghuabigdata.com ")
  exit()

ScpStatus = 1
count = 0
while (ScpStatus != 0 & count < 5):
  os.system("ssh -p 55556 root@182.150.*.* \"mkdir -p /data/hecran/hbase/increment/\"")
  ScpStatus = os.system("scp -P 55556 " + tarFile + " root@182.150.*.*:/data/hecran/hbase/increment/")
  count = count + 1

if(count != 5):
  os.system("rm -rf /root/increment/*")
  os.system("rm -rf " + tarFile)
  os.system("echo \"$(date +%Y-%m-%d) 01:00:00,000\" > /root/lastImportDate")
  RunRemoteSH="ssh -p 55556 root@182.150.*.* 'bash /root/chenyao increment'"
  os.system(RunRemoteSH)
else:
  os.system("echo \"RemoteServer [172.16.6.10] count is 5\" | /bin/mailx -s \"Hbase_dump OnLine ERROR\" biqin@tsinghuabigdata.com")
  exit()
