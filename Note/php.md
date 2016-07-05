下载&&解压
```
[rot@localhost]# cd /usr/local/src
[root@localhost src]# wget http://hk1.php.net/distributions/php-5.4.45.tar.bz2 
[root@localhost src]# tar zvxf php-5.4.45.tar.gz
```
配置编译参数
```
[root@localhost src]# cd php-5.4.45
[root@localhost php-5.4.45]# ./configure \
--prefix=/usr/local/php \
--with-apxs2=/usr/local/apache2/bin/apxs \
--with-config-file-path=/usr/local/php/etc \
--with-mysql=/usr/local/mysql \
--with-libxml-dir \
--with-gd \
--with-jpeg-dir \
--with-png-dir \
--with-freetype-dir \
--with-iconv-dir \
--with-zlib-dir \
--with-bz2 \
--with-openssl \
--with-mcrypt \
--enable-soap \
--enable-gd-native-ttf \
--enable-mbstring \
--enable-sockets \
--enable-exif \
--disable-ipv6
```
> 常见错误

1. configure: error: xml2-config not found. Please check your libxml2 installation
    yum install -y libxml2-devel
2. configure: error: Cannot find OpenSSL's <evp.h> 
    yum install -y openssl openssl-devel
3. checking for BZip2 in default path... not found
  configure: error: Please reinstall the BZip2 distribution 
    yum install -y bzip2 bzip2-devel
4. configure: error: png.h not found.
    yum install -y libpng libpng-devel
5. configure: error: freetype.h not found
    yum install -y freetype freetype-devel
6. configure: error: mcrypt.h not found. Please reinstall libmcrypt    因为centos6.x 默认的yum源没有libmcrypt-devel 这个包，只能借助第三方yum源。
    yum install -y  libmcrypt-devel
7. configure: error: jpeglib.h not found
    yum install -y libjpeg-devel

编译安装
`[root@localhost php-5.4.45]# make && make install`
拷贝配置文件 
`[root@localhost php-5.4.45]# cp php.ini-production /usr/local/php/etc/php.ini`
```
php-fpm.conf
[global]
pid = /usr/local/php-5.5.25/var/run/php-fpm.pid
error_log = /usr/local/php-5.5.25/var/log/php-fpm.log
log_level = notice
 
[www]
listen = 9000
#listen.backlog = -1
#listen.allowed_clients = 127.0.0.1
#listen.owner = root
#listen.group = root
#listen.mode = 0666
user = nobody
group = nobody
pm = dynamic
pm.max_children = 100
pm.start_servers = 20
pm.min_spare_servers = 5
pm.max_spare_servers = 35
pm.max_requests = 10240
request_terminate_timeout = 100
request_slowlog_timeout = 0
slowlog = var/log/slow.log
```
