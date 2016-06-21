#!/bin/bash

############conf############
CY_HADOOP_USER="root"
CY_HADOOP_HOME="/home/hadoop/hadoop"
CY_HBASES_HOME="/home/hadoop/hbase"

###########advanced conf###########
RemoteServer="172.16.6.10"
# SSHPORT="22"
# USERNAME="root"

Usage(){
    echo """
    ${0} ${increment/full}

    like this:
        ${0} increment #<= this will be import <$(date -d 'yesterday' +%Y-%m-%d)> increment data
    or:
        ${0} full      #<= this will be import <$(date -d 'yesterday' +%Y-%m-%d)> full data
    """
}

rootness(){
    if [[ $EUID -ne 0 ]]; then
        erro_mssg "This script must be run as root"
    fi
}

init(){
    default_path=/home/hbase_import
    scp_path=${default_path}/scp
    tmp_path=${default_path}/tmp
    full_path=${default_path}/full
    increment_path=${default_path}/increment
    mkdir -p ${default_path} ${scp_path} ${tmp_path} ${full_path} ${increment_path}
    chown -R nobody.nobody ${default_path}
}

TimeRun(){
    ${*}&
    id=$!
    char=("-" "/" "|" "\\")
    n=0
    while ps ax | grep "^[[:space:]]*${id}" > /dev/null
    do
        echo -ne "\rChenYao is hard working... ${char[$n]}"
        n=$(( (n+1)%4 ))
        sleep 1
    done
    # wait ${id}
    echo -e "\nDone ."
}

info_mssg(){
    echo -e "\033[32m==> ${1} \033[0m"
}

erro_mssg(){
    echo -e "\033[31m==> ${1} \033[0m"
    exit 1
}

pause(){
    read -n 1 -p "$*" INP
    if [[ "$INP" != "" ]]; then
        echo -ne '\b \n'
    fi
}

ScpHbaseDataToLocal(){
    local SRC=${1}
    local DES=${2:-${default_path}/${RunType}}
    if [[ -d ${default_path}/${RunType} ]];then
        info_mssg "Clean Dir <${default_path}/${RunType}/>"
        rm -rf ${default_path}/${RunType}/*
    fi
    if [[ ! -e "${DES}/${SRC##*/}" ]];then
        info_mssg "Copy <${RemoteServer}:${SRC}> to <${DES}> "
        TimeRun scp -r -P ${SSHPORT:-22} ${USERNAME:-root}@${RemoteServer}:${SRC} ${DES}
        if [[ "${?}" != "0" ]]; then erro_mssg "SCP FAILE";fi
    else
        info_mssg "Already exists: <${default_path}/${RunType}/${RunType}.${ImportDate}.tar.gz> "
    fi
}

tyttar(){
    info_mssg "Start untar <${default_path}/${RunType}/${RunType}.${ImportDate}.tar.gz>"
    if [[ -e ${default_path}/${RunType}/${RunType}.${ImportDate}.tar.gz ]];then
        # if [[ ! -d ${default_path}/${RunType}/${RunType} ]];then
        #     cd ${default_path}/${RunType}/ && TimeRun tar zxf ${RunType}.${ImportDate}.tar.gz
        # else
        #     info_mssg "Already exists: ${default_path}/${RunType}/${RunType}"
        # fi
        if [[ -d ${default_path}/${RunType}/${RunType} ]];then
            info_mssg "Already exists: <${default_path}/${RunType}/${RunType}>"
            info_mssg "Now clean it <${default_path}/${RunType}/${RunType}>"
            rm -rf ${default_path}/${RunType}/${RunType}
        fi
        cd ${default_path}/${RunType}/ && TimeRun tar zxf ${RunType}.${ImportDate}.tar.gz
    else
        erro_mssg "NO FOUND <${default_path}/${RunType}/${RunType}.${ImportDate}.tar.gz> "
    fi
}

copyFromLocal(){
    info_mssg "Start copyFromLocal <${default_path}/${RunType}/${RunType} => /hbase_dump>"
    # DFS_CMD="${CY_HADOOP_HOME}/bin/hdfs dfs \-copyFromLocal ${default_path}/${RunType}/${RunType} /hbase_dump"
    # TimeRun "/sbin/runuser -l ${CY_HADOOP_USER} -c "${DFS_CMD}""
    /sbin/runuser -l ${CY_HADOOP_USER} -c "${CY_HADOOP_HOME}/bin/hdfs dfs -rm -r /hbase_dump/${RunType}/*"
    /sbin/runuser -l ${CY_HADOOP_USER} -c "${CY_HADOOP_HOME}/bin/hdfs dfs -copyFromLocal ${default_path}/${RunType}/${RunType} /hbase_dump"
    # if [[ -d "${default_path}/${RunType}/${RunType}" ]];then
    #     rm -rf ${default_path}/${RunType}/${RunType}
    # fi
}

copyToLocal(){
    local DIR=${1:-"/hbase"}
    local TODIR=${2:-"/data/hecran/hbase/tmp"}
    info_mssg "Start copyToLocal <${DIR} => ${TODIR}>"
    /sbin/runuser -l ${CY_HADOOP_USER} -c "${CY_HADOOP_HOME}/bin/hdfs dfs -copyToLocal ${DIR} ${TODIR}"
}

importDefault(){
    for table in ${tables[@]}; do
        info_mssg "Now import table: <${table}>"
        /sbin/runuser -l ${CY_HADOOP_USER} -c "${CY_HBASES_HOME}/bin/hbase org.apache.hadoop.hbase.mapreduce.Import ${table} /hbase_dump/${RunType}/${ImportDate}/${table}"
    done
}

exportDefault(){
    for table in ${tables[@]}; do
        info_mssg "Now Export table: <${table}>"
        /sbin/runuser -l ${CY_HADOOP_USER} -c "${CY_HBASES_HOME}/bin/hbase org.apache.hadoop.hbase.mapreduce.Export ${table} /hbase_dump/full/${ImportDate}/${table} 1"
    done

}


RunCheck(){

    info_mssg "Import type: <${RunType}> "

    if [[ "${CY_HADOOP_USER}" == "" ]];then
        erro_mssg "HADOOP USER IS NULL"
    fi
    info_mssg "Hadoop user: <${CY_HADOOP_USER}>"

    if [[ "${CY_HADOOP_HOME}" == "" ]];then
        if [[ -e "/home/${CY_HADOOP_USER}/.bashrc" ]];then
            source /home/${CY_HADOOP_USER}/.bashrc
        elif [[ -e "/${CY_HADOOP_USER}/.bashrc" ]]; then
            source /${CY_HADOOP_USER}/.bashrc
        else
            erro_mssg "CAN NOT LOAD ${CY_HADOOP_USER}/.bashrc"
        fi
    fi
    if [[ ! -d "${HADOOP_HOME}/bin" ]] || [[ ! -d "${CY_HADOOP_HOME}/bin" ]];then
        erro_mssg "\${HADOOP_HOME} is NULL"
    fi
    CY_HADOOP_HOME=${CY_HADOOP_HOME:-${HADOOP_HOME}}
    info_mssg "Hadoop home: <${CY_HADOOP_HOME}>"



    scp -r -P ${SSHPORT:-22} ${USERNAME:-root}@172.16.6.9:/data/hecran/hbase/synTables ${default_path} &>/dev/null
    scp -r -P ${SSHPORT:-22} ${USERNAME:-root}@172.16.6.9:/data/hecran/hbase/createTables ${default_path} &>/dev/null
    if [[ -e "${default_path}/synTables" ]];then
        info_mssg "Get table from <${default_path}/synTables>"
        tables=$(cat ${default_path}/synTables)
    else
        info_mssg "No found synTables , now use default conf."
        tables=("Check_Result" "Class_Exam_Statistic" "Class_Score_Rank_Statistic" "Formula_Recognition_Result" "Grade_Score_Rank_Statistic" "Message" "Paper_Info" "Pen_Data" "Pre_SameType_Exam" "Rank_Statistic" "Recognition_Result" "Score_Result" "Score_Result_Original" "Stroke_Info" "Student_Analysis_Result" "Student_Analysis_Result_Original" "Student_Error_Type_Statistic" "Student_Exam_Statistic" "Student_Failed_Question" "Student_Failed_Quiz" "Student_Integral_Statistic" "Student_Knowledge_Statistic" "Student_Question_Accuracy_Statistic" "Student_Question_Statistic" "Student_Score_Rank_Statistic" "class" "erAction_real" "error_question_collection" "etl_config" "etl_data_source" "etl_fields_mapping" "etl_keystep_success" "etl_log" "etl_status" "etl_table_mapping" "examination" "exerhome" "exerhome_question_source" "gradedict" "log_error_analysis" "log_error_orignal" "log_error_orignal_back" "patriarch" "resource_manager" "resource_manager_indexing" "right_question_collection" "school" "student" "student_error_question_collection" "student_error_question_collection_detail" "student_patriarch_relation" "support_home_detail_report" "support_home_exam_task" "support_home_user_detail_report" "teacher")
    fi
}

fullback(){
    rootness
    copyToLocal "/hbase" "/data/hecran/hbase/tmp"
    info_mssg "start tar backfiles"
    cd /data/hecran/hbase/tmp ||  exit 15
    tar czf full.$(date +%Y-%m-%d).tar.gz hbase
    mv full.$(date +%Y-%m-%d).tar.gz /data/hecran/hbase/full
    if [[ -d "/data/hecran/hbase/full" ]];then
        cd /data/hecran/hbase/full ||  exit 15
        find . -type f -mtime +2 |xargs rm -f
    fi
    if [[ -d "/data/hecran/hbase/increment" ]];then
        cd /data/hecran/hbase/increment ||  exit 15
        find . -type f -mtime +10 |xargs rm -f
    fi
    rm -rf /data/hecran/hbase/tmp/*
}


CreateHbaseTables(){

    if [[ -f ${default_path}/createTables ]]; then
        cat ${default_path}/createTables | while read line ; do
            echo "create ${line}" | /sbin/runuser -l ${CY_HADOOP_USER} -c "${CY_HBASES_HOME}/bin/hbase shell" 2> /dev/null
        done
    fi
}

increment_import(){
    rootness
    init
    RunCheck
    ScpHbaseDataToLocal "/data/hecran/hbase/${RunType}/${RunType}.${ImportDate}.tar.gz"
    CreateHbaseTables
    tyttar
    copyFromLocal
    importDefault
}

full_import(){
    echo """

        Now will destroy current data

    """
    pause 'Press any key to continue...'
    rootness
    init
  #  RunCheck
  #  ScpHbaseDataToLocal "/data/hecran/hbase/${RunType}/${RunType}.${ImportDate}.tar.gz"
  #  tyttar
  #  copyFromLocal
    info_mssg "Destroy /hbase data"
    /sbin/runuser -l ${CY_HADOOP_USER} -c "${CY_HADOOP_HOME}/bin/hdfs dfs -rm -r /hbase/*"
    info_mssg "Copy </hbase_dump/${RunType}/${ImportDate}> to </hbase>"
    /sbin/runuser -l ${CY_HADOOP_USER} -c "${CY_HADOOP_HOME}/bin/hdfs dfs -cp /hbase_dump/${RunType}/${ImportDate}/* /hbase"
}

source /etc/profile
mkdir -p /root/hbaselog
log_files="/root/hbaselog/$(date +%Y-%m-%d).log"
echo "=== $(date +%Y-%m-%d-%H:%M:%S) ===" >> ${log_files}

case ${1} in
  increment ) RunType=${1} && ImportDate=${2:-$(date -d 'yesterday' +%Y-%m-%d)} && increment_import 2>&1 | tee -a ${log_files} ;;
  full ) RunType=${1} && ImportDate=${2:-$(date -d 'yesterday' +%Y-%m-%d)} && full_import 2>&1 | tee -a ${log_files} ;;
  # autoexport ) autoexport 2>&1 | tee -a ${log_files} ;;
  FULLBACK ) fullback 2>&1 | tee -a ${log_files} ;;
  * )  Usage 2>&1 | tee -a ${log_files} ;;
esac
