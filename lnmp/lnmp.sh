#!/bin/bash

cwd=$(pwd)
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
#######Begin########
echo "It will install lnmp."
sleep 1
##check last command is OK or not.
check_ok() {
if [ $? != 0 ]
then
    echo "Error, Check the error log."
    exit 1
fi
}
##get the archive of the system,i686 or x86_64.
##close seliux
sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
selinux_s=`getenforce`
if [ $selinux_s == "enforcing" ]
then
    setenforce 0
fi
##close iptables
iptables-save > /etc/sysconfig/iptables_`date +%s`
iptables -F
service iptables save

##if the packge installed ,then omit.
myum() {
if ! rpm -qa|grep -q "^$1"
then
    yum install -y $1
    check_ok
else
    echo $1 already installed.
fi
}

## install some packges.
for p in gcc wget perl perl-devel libaio libaio-devel pcre-devel zlib-devel cmake ncurses-devel gcc-c++ openssl openssl-devel
do
    myum $p
done

##install epel.
if rpm -qa epel-release >/dev/null
then
    rpm -e epel-release
fi
if ls /etc/yum.repos.d/epel-6.repo* >/dev/null 2>&1
then
    rm -f /etc/yum.repos.d/epel-6.repo*
fi
wget -P /etc/yum.repos.d/ http://mirrors.aliyun.com/repo/epel-6.repo


##function of installing mysqld.
install_mysqld() {
    cd /usr/local/src
    [ -f mysql-5.5.52.tar.gz ] || \cp ${cwd}/tar/mysql-5.5.52.tar.gz .
    tar zxf mysql-5.5.52.tar.gz
    check_ok
    cd mysql-5.5.52
    cmake \
    -DCMAKE_INSTALL_PREFIX=/usr/local/mysql \
    -DMYSQL_DATADIR=/data/mysqldata \
    -DSYSCONFDIR=/usr/local/mysql/etc \
    -DMYSQL_UNIX_ADDR=/tmp/mysql.sock \
    -DWITH_MYISAM_STORAGE_ENGINE=1 \
    -DWITH_INNOBASE_STORAGE_ENGINE=1 \
    -DENABLED_LOCAL_INFILE=1 \
    -DWITH_PARTITION_STORAGE_ENGINE=1 \
    -DEXTRA_CHARSETS=all \
    -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci
    check_ok
    make && make install
    check_ok
    if ! grep '^mysql:' /etc/passwd
    then
    useradd -M mysql -s /sbin/nologin
    fi
    myum compat-libstdc++-33
    mkdir -p /data/mysqldata
    chown -R mysql:mysql /data/mysqldata
    cd /usr/local/mysql
    ./scripts/mysql_install_db --user=mysql --datadir=/data/mysqldata
    check_ok
    cd ${cwd}
    \cp conf/my.cnf /etc/my.cnf
    \cp init/mysqld /etc/init.d/mysqld
    chmod 755 /etc/init.d/mysqld
    chkconfig --add mysqld
    chkconfig mysqld on
    mkdir /usr/local/mysql/logs
    service mysqld start
    check_ok
    break
}



##function of check service is running or not, example nginx, php-fpm.
check_service() {
if [ "$1" == "phpfpm" ]
then
    s="php-fpm"
else
    s=$1
fi
n=`ps aux |grep "$s"|wc -l`
if [ $n -gt 1 ]
then
    echo "$1 service is already started."
else
    if [ -f /etc/init.d/$1 ]
    then
        /etc/init.d/$1 start
        check_ok
    else
        install_$1
    fi
fi
}


##function of install nginx
install_nginx() {
    cd /usr/local/src
    [ -f nginx-1.4.4.tar.gz ] || \cp ${cwd}/tar/nginx-1.4.4.tar.gz .
    tar zxf nginx-1.4.4.tar.gz
    cd nginx-1.4.4
    myum pcre-devel
    ./configure \
    --prefix=/usr/local/nginx \
    --with-http_stub_status_module \
    --with-http_ssl_module \
    --with-http_gzip_static_module \
    --with-http_sub_module \
    --with-pcre
    check_ok
    make && make install
    check_ok
    if [ -f /etc/init.d/nginx ]
    then
        /bin/mv /etc/init.d/nginx  /etc/init.d/nginx_`date +%s`
    fi
    cd ${cwd}
    \cp init/nginx /etc/init.d/nginx
    \cp conf/nginx.conf  /usr/local/nginx/conf/nginx.conf
    check_ok
    chmod 755 /etc/init.d/nginx
    chkconfig --add nginx
    chkconfig nginx on
    check_ok
    service nginx start
    check_ok
    mkdir /home/www
    echo -e "<?php\n    phpinfo();\n?>" > /home/www/index.php
    check_ok
}

##function of install php-fpm
install_phpfpm() {
    cd /usr/local/src/
    [ -f php-5.5.25.tar.gz ] || \cp ${cwd}/tar/php-5.5.25.tar.gz .
    tar zxf php-5.5.25.tar.gz &&   cd php-5.5.25
    for p in  openssl-devel bzip2-devel \
    libxml2-devel curl-devel libpng-devel \
    libjpeg-devel freetype-devel libmcrypt-devel\
    libtool-ltdl-devel perl-devel
    do
        myum $p
    done

    if ! grep -q '^php-fpm:' /etc/passwd
    then
        useradd -M -s /sbin/nologin php-fpm
    fi
    check_ok
    ./configure --prefix=/usr/local/php --enable-opcache --with-config-file-path=/usr/local/php/etc --with-mysql=mysqlnd --with-mysqli=mysqlnd --with-pdo-mysql=mysqlnd --enable-fpm --enable-fastcgi --enable-static --enable-inline-optimization --enable-sockets --enable-wddx --enable-zip --enable-calendar --enable-bcmath --enable-soap --with-zlib --with-iconv --with-gd --with-xmlrpc --enable-mbstring --without-sqlite --with-curl --enable-ftp --with-mcrypt --with-freetype-dir --with-jpeg-dir --with-png-dir --disable-ipv6 --disable-debug --with-openssl --disable-maintainer-zts --disable-safe-mode --disable-fileinfo
    check_ok
    make && make install
    check_ok
    cd ${cwd}
    [ -f /usr/local/php/etc/php.ini ] || \cp conf/php.ini  /usr/local/php/etc/php.ini
    if /usr/local/php/bin/php -i |grep -iq 'date.timezone => no value'
    then
        sed -i '/;date.timezone =$/a\date.timezone = "Asia\/Chongqing"'  /usr/local/php/etc/php.ini
        check_ok
    fi
    [ -f /usr/local/php/etc/php-fpm.conf ] || \cp conf/php-fpm.conf /usr/local/php/etc/php-fpm.conf
    check_ok
    [ -f /etc/init.d/phpfpm ] || \cp init/php-fpm /etc/init.d/phpfpm
    chmod 755 /etc/init.d/phpfpm
    chkconfig phpfpm on
    install_redis
    install_phpredis
    service phpfpm start
    check_ok
    break
}

##function of install redis
install_redis(){
    cd /usr/local/src
    [ -f redis-3.0.7.tar.gz ] || \cp ${cwd}/tar/redis-3.0.7.tar.gz .
    tar zxf redis-3.0.7.tar.gz && cd redis-3.0.7
    make
    check_ok
    make PREFIX=/usr/local/redis install
    check_ok
    cd ${cwd}
    mkdir /usr/local/redis/{etc,var}
    \cp conf/redis.conf /usr/local/redis/etc/redis.conf
    /usr/local/redis/bin/redis-server /usr/local/redis/etc/redis.conf
    check_ok
}

##function of install phpredis
install_phpredis(){
    cd /usr/local/src
    [ -f phpredis.tar.gz ] || \cp ${cwd}/tar/phpredis.tar.gz .
    tar zxf phpredis.tar.gz
    cd phpredis
    /usr/local/php/bin/phpize
    check_ok
    ./configure --with-php-config=/usr/local/php/bin/php-config
    check_ok
    make && make install
    check_ok
    mv /usr/local/php/lib/php/extensions/no*/*.so /usr/lib64/
}
##function of install lnmp
lnmp() {
check_service mysqld
check_service nginx
check_service phpfpm
echo "export PATH=\$PATH:/usr/local/mysql/bin:/usr/local/redis/bin:/usr/local/php/sbin:/usr/local/php/bin:/usr/local/nginx/sbin" >> /etc/profile
source /etc/profile
echo "The lnmp done, Please use 'http://your ip/index.php' to access."
}

read -p "Please enter what you want install  (lnmp|mysql|nginx|phpfpm|redis)" t
case $t in

    lnmp)
        lnmp
        ;;
    mysql)
        check_service mysqld
        ;;
    nginx)
        check_service nginx
        ;;
    phpfpm)
        check_service phpfpm
        ;;
    redis)
        install_redis
        ;;
    *)
        echo "Only 'yes' your can input."
        ;;
esac
##########end##############
