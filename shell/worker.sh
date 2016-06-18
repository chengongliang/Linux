
# 注意:
#      =号后面的值必须用双引号 " "

#########
#这里是worker以前的command的值
#########
WORKER_NAME="cut"

#########
#class名字
#########
CLASS="com.tsinghuabigdata.edu.worker.BeeWorkerLauncher"


#########
#jvm参数
#########
JVM_OPTS="-server -Xms3g -Xmx3g -Xmn2g -XX:SurvivorRatio=4  -XX:+UseCMSInitiatingOccupancyOnly  -XX:CMSInitiatingOccupancyFraction=80 -XX:+UseMembar -XX:+UseConcMarkSweepGC"

#########
#邮件告警默认提供.log及.out最后15行日志,建议相关负责人添加自己的邮箱
#添加格式为: 
#mail_notice="a@tsinghuabigdata.com cc@tsinghuabigdata.com 1111@tsinghuabigdata.com"
#########
MAIL_NOTICE=""