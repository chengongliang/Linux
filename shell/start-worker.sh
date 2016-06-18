#!/bin/bash
source /etc/profile

Usage(){
    echo """
        ${0} student|class|statistic start|stop|status

        congfig:
            plz edit conf/worker.conf before use ${0} .

        use like this:
            ${0} statistic start        #<= this will be start statistic worker .
            ${0} statistic start daemon #<= this will be start statistic worker with daemon.
            ${0} statistic stop         #<= this will be stop statistic worker .
    """
}

# load system func
if [[ -f "/lib/lsb/init-functions" ]]; then
    . /lib/lsb/init-functions
else
    log_success_msg(){ 
        echo -e "\033[32m--> SUCCESS!\033[0m $@" 
    }
    log_failure_msg(){ 
        echo -e "\033[31m--> ERROR!\033[0m $@"
        #exit 1
    }
fi

# if [[ $EUID -ne 0 ]]; then
#     log_failure_msg "This script must be run as root"
# fi

# load conf 
DAEMON_HOME=$(cd $(dirname ${0})>/dev/null;pwd)
WORKER_HOME=${DAEMON_HOME%/*}

if [[ ! -f "${DAEMON_HOME}/worker.conf" ]]; then
    log_failure_msg "Couldn't find conf <${WORKER_HOME}/worker.conf>"
    exit 1
else
    # load ${WORKER_NAME} ${CLASS} ${JVM_OPTS} ${JAVA_OPTS}
    . ${DAEMON_HOME}/worker.conf
fi

if [[ "${JVM_OPTS}" == "" ]]; then
    log_failure_msg "<worker.conf> JVM_OPTS is null ."
    exit 1
else
    WORKER_LOG_DIR="${WORKER_HOME}/logs"
    WORKER_LOG_FILE="${WORKER_NAME}-worker.log"
    WORKER_OUT_FILE="${WORKER_NAME}-worker.out"
    WORKER_PID_FILE="${WORKER_LOG_DIR}/${WORKER_NAME}.pid"
    #hecran
    ServiceStartupTimeout="20"
    DEMON_PID_FILE="${WORKER_LOG_DIR}/daemon.PID"
    JAVA_OPTS="${JVM_OPTS} -Dworker.log.dir=${WORKER_LOG_DIR} -Dworker.log.file=${WORKER_LOG_FILE}"
fi

if [[ "${JAVA_OPTS}" == "" ]]; then
    log_failure_msg "<worker.conf> JAVA_OPTS is null ."
    exit 1
fi

if [[ "${CLASS}" == "" ]] ; then
    log_failure_msg "<worker.conf> CLASS is null ."
    exit 1
fi

WORKER_LOG_DIR="${WORKER_HOME}/logs"
WORKER_LOG_FILE="${WORKER_NAME}-worker.log"
WORKER_OUT_FILE="${WORKER_NAME}-worker.out"
WORKER_PID_FILE="${WORKER_LOG_DIR}/${WORKER_NAME}.pid"
#hecran
ServiceStartupTimeout="20"
DEMON_PID_FILE="${WORKER_LOG_DIR}/daemon.PID"


if [[ ! -d "${WORKER_LOG_DIR}" ]]; then
    mkdir "${WORKER_LOG_DIR}"
fi

CLASSPATH=${WORKER_HOME}/conf
CLASSPATH=${CLASSPATH}:${WORKER_HOME}

for f in ${WORKER_HOME}/*.jar; do
    CLASSPATH=${CLASSPATH}:$f
done

for f in ${WORKER_HOME}/lib/*.jar; do
    CLASSPATH=${CLASSPATH}:$f
done


# case $(echo "testing\c"),$(echo -n testing) in
#     *c*,-n*) echo_n=   echo_c=     ;;
#     *c*,*)   echo_n=-n echo_c=     ;;
#     *)       echo_n=   echo_c='\c' ;;
# esac


    # while test $i -ne ${ServiceStartupTimeout} ; do

    #     if test -n "${WorkerPidNumb}"; then
    #         if kill -0 "${WorkerPidNumb}" 2>/dev/null; then
    #             :
    #         else
    #             if test -n "$avoid_race_condition"; then
    #                 avoid_race_condition=""
    #                 continue 
    #             fi
    #             log_failure_msg "The server quit ."
    #             return 1 
    #         fi
    #     fi

    #     echo $echo_n ".$echo_c"
    #     i=`expr $i + 1`
    #     sleep 1

    # done

Start(){
    if [ -f ${WORKER_PID_FILE} ]; then
        TARGET_ID="$(cat "${WORKER_PID_FILE}")"
        if [[ $(ps -p "$TARGET_ID" -o args=) =~ ${WORKER_NAME} ]]; then
            log_failure_msg "${WORKER_NAME} running as process $TARGET_ID.  Stop it first."
            exit 1
        fi
    fi
    log_success_msg "starting ${WORKER_NAME}"
    nohup java -Dproc_${WORKER_NAME} -cp $CLASSPATH  -XX:OnOutOfMemoryError="kill -9 %p" $JAVA_OPTS $CLASS ${WORKER_NAME} ${PROPERTIES} > $WORKER_LOG_DIR/$WORKER_OUT_FILE  2>&1 &
    echo $! > ${WORKER_PID_FILE}


    if [[ "${1}" == "daemon" ]]; then
        nohup bash ${DAEMON_HOME}/WorkerDaemon DaemonStart >/dev/null 2>&1 &
    fi
}

Stop(){

    if [[ -f "${DEMON_PID_FILE}" ]]; then
        DEMON_PID=$(cat ${DEMON_PID_FILE})
        if kill -0 ${DEMON_PID} 2>/dev/null ; then
            kill -9 ${DEMON_PID}
        rm -rf ${DEMON_PID_FILE}
        else
            rm -rf ${DEMON_PID_FILE}
        fi
    fi

    if [ -f ${WORKER_PID_FILE} ]; then
        TARGET_ID="$(cat ${WORKER_PID_FILE})"
        if [[ $(ps -p "$TARGET_ID" -o comm=) =~ "java" ]]; then
            log_success_msg "stopping ${WORKER_NAME}"
            kill "$TARGET_ID" && rm -f "${WORKER_PID_FILE}"
        else
            log_success_msg "no ${WORKER_NAME} to stop, but ${WORKER_PID_FILE} exist, remove it"
            rm -f "${WORKER_PID_FILE}"
        fi
    else
        echo "no ${WORKER_NAME} to stop"
    fi
}

Status(){
    if [ -f ${WORKER_PID_FILE} ]; then
        TARGET_ID="$(cat "${WORKER_PID_FILE}")"
        if [[ $(ps -p "$TARGET_ID" -o comm=) =~ "java" ]]; then
            echo "${WORKER_NAME} is running"
        else
            echo "no ${WORKER_NAME} to stop, but ${WORKER_PID_FILE} exist, remove it"
            rm -f "${WORKER_PID_FILE}"
        fi
    else
        echo "${WORKER_NAME} stoped"
    fi
}

case ${1} in
    start ) Start ${2} ;;
    stop ) Stop ;;
    status ) Status ;;
    * )  Usage ;;
esac