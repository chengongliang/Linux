apache官网下载地址：`http://www.apache.org/dyn/closer.cgi`
###下载
```
[root@localhost mysql]# cd /usr/local/src/
[root@localhost src]# wget  http://mirrors.hust.edu.cn/apache/httpd/httpd-2.4.20.tar.gz 
[root@localhost src]# tar zvxf httpd-2.4.20.tar.gz
```
###编译
```
[root@localhost src]# cd httpd-2.4.20
[root@localhost httpd-2.4.20]# ./configure \
--prefix=/usr/local/apache2 \
--with-included-apr \
--enable-so \
--enable-deflate=shared \
--enable-expires=shared \
--enable-rewrite=shared \
--with-pcre
--prefix 指定安装到哪里， --enable-so 表示启用DSO 
--enable-deflate=shared 表示共享的方式编译deflate，后面的参数同理。
```
* 如果这一步出现了这样的错误:
*error: mod_deflate has been requested but can not be built due to prerequisite failures*

解决办法
`yum install -y zlib-devel`
为了避免在make的时候出现错误，最好提前先安装好一些库文件:
`yum install -y pcre pcre-devel apr apr-devel`
##安装
```
[root@localhost httpd-2.4.20]# make
[root@localhost httpd-2.4.20]# make install
```
使用 echo $? 来检查是否正确执行，否则根据错误提示去解决问题。
