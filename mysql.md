MySQL官网下载地址 `http://dev.mysql.com/downloads/`

>先删除原有MySQL，再进行源码安装
rpm -qa|grep mysql
yum remove mysql-libs-5.1.73-5.el6_6.i686

#安装步骤：

##下载解压
```
cd /usr/local/src/
wget http://mirrors.sohu.com/mysql/MySQL-5.1/mysql-5.1.73-linux-i686-glibc23.tar.gz 
tar zxvf /usr/local/src/mysql-5.1.73-linux-i686-icc-glibc23.tar.gz
把解压完的数据移动到/usr/local/mysql
mv mysql-5.1.73-linux-i686-icc-glibc23 /usr/local/mysql
```
##建立mysql用户
`[root@localhost src]# useradd -s /sbin/nologin -M mysql`
##初始化数据库
```
[root@localhost src]# cd /usr/local/mysql
[root@localhost mysql]# mkdir -p /data/mysql ; chown -R mysql:mysql /data/mysql
[root@localhost mysql]# ./scripts/mysql_install_db --user=mysql --datadir=/data/mysql
  --user 定义数据库的所属主， --datadir 定义数据库安装到哪里，建议放到大空间的分区上，这个目录需要自行创建。关键步骤，看到两个 “OK” 说明执行正确
```
##拷贝配置和启动脚本
```
[root@localhost mysql]# cp support-files/my-large.cnf /etc/my.cnf
[root@localhost mysql]# cp support-files/mysql.server /etc/init.d/mysqld
[root@localhost mysql]# chmod 755 /etc/init.d/mysqld
修改启动脚本
[root@localhost mysql]# vim /etc/init.d/mysqld     #需要修改的地方有 “basedir=/usr/local/mysql datadir=/data/mysql” （前面初始化数据库时定义的目录）
```
把启动脚本加入系统服务项，并设定开机启动，启动mysql
```
[root@localhost mysql]# chkconfig --add mysqld
[root@localhost mysql]# chkconfig mysqld on
[root@localhost mysql]# service mysqld start
```
* 如果启动不了，到 /data/mysql/ 下查看错误日志，这个日志通常是主机名.err. 检查mysql是否启动的命令为:
[root@localhost mysql]# ps aux |grep mysqld
##设置初始密码 
mysqladmin -uroot password '920402'
