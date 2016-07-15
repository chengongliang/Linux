#!/bin/bash

#for 100.31
#for 100.31

#name
NAMEE="100.11"
#remote cmd run
PORT="54321"
IP="192.168.100.3"
USER="root"

#local path
syn_home="/data/mysql_db_back"
TARLOG="${syn_home}/opt.log"

#remote path
HOMEE="/home/hecran/mysql-5.5.20-30306/mysqldataback/${NAMEE}"
CCMD="bash /home/hecran/mysql-5.5.20-30306/mysqldataback/import.sh ${NAMEE}"

#g
TIME=`date +%m-%d-%Y`
TAR="${TIME}.tar.gz"

#get sql name
SQL=`cd ${syn_home} && ls *.sql`

# sed ^@ => ""
if [[ ${SQL} == "" ]] ; then
  echo "no sql"
  exit 1
fi
for i in ${SQL} ; do
  sed -i 's/\o000//g' ${i}
done

#run !
if [[ ${SQL} != "" ]] ; then
  cd ${syn_home} && tar czf ${TAR} ${SQL}
else
  echo "${TIME} - ERRO -no ${SQL} files ! " >> ${TARLOG}
  exit 1
fi

if [ -f ${syn_home}/${TAR} ];then
  mv ${TAR} tar/
  find tar/*.tar.gz -mtime +3 -print | xargs rm -rf
  ssh -p ${PORT} ${USER}@${IP} "mkdir -p ${HOMEE}"
  scp -P ${PORT} tar/${TAR} ${USER}@${IP}:${HOMEE}
  ssh -p ${PORT} ${USER}@${IP} "${CCMD}"
else
  echo "${TIME} - ERRO -no ${TAR} files ! " >> ${TARLOG}
  exit 1
fi
