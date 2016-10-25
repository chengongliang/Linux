#!/usr/bin/env python
#coding:utf8

import os
import sys
import pycurl

def main(url):
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.CONNECTTIMEOUT, 5)
    c.setopt(pycurl.TIMEOUT, 5)
    c.setopt(pycurl.NOPROGRESS, 1)
    c.setopt(pycurl.FORBID_REUSE, 1)
    c.setopt(pycurl.MAXREDIRS, 1)
    c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)
    indexfile = open(os.path.dirname(os.path.realpath(__file__)) + "/content.txt", "wb")
    c.setopt(pycurl.WRITEHEADER, indexfile)
    c.setopt(pycurl.WRITEDATA, indexfile)

    try:
        c.perform()
    except Exception, e:
        print "connection error: " + str(e)
        indexfile.close()
        c.close()
        sys.exit()

    NAMELOOKUP_TIME = c.getinfo(c.NAMELOOKUP_TIME) #获取DNS解析时间
    CONNECT_TIME = c.getinfo(c.CONNECT_TIME)  #获取建立连接时间
    PRETRANSFER_TIME = c.getinfo(c.PRETRANSFER_TIME)  #获取从建立连接到准备传输消耗时间
    STARTTRANSFER_TIME = c.getinfo(c.STARTTRANSFER_TIME) #获取从建立连接到传输开始消耗的时间
    TOTAL_TIME = c.getinfo(c.TOTAL_TIME) #获取传输的总时间
    HTTP_CODE = c.getinfo(c.HTTP_CODE) #获取HTTP状态码
    SIZE_DOWNLOAD = c.getinfo(c.SIZE_DOWNLOAD) #获取下载数据包大小
    HEADER_SIZE = c.getinfo(c.HEADER_SIZE) #获取HTTP头部大小
    SPEED_DOWNLOAD=c.getinfo(c.SPEED_DOWNLOAD) #获取平均下载速度
    #打印输出相关数据
    print "HTTP状态码：%s" %(HTTP_CODE)
    print "DNS解析时间：%.2f ms"%(NAMELOOKUP_TIME*1000)
    print "建立连接时间：%.2f ms" %(CONNECT_TIME*1000)
    print "准备传输时间：%.2f ms" %(PRETRANSFER_TIME*1000)
    print "传输开始时间：%.2f ms" %(STARTTRANSFER_TIME*1000)
    print "传输结束总时间：%.2f ms" %(TOTAL_TIME*1000)
    print "下载数据包大小：%d bytes/s" %(SIZE_DOWNLOAD)
    print "HTTP头部大小：%d byte" %(HEADER_SIZE)
    print "平均下载速度：%d bytes/s" %(SPEED_DOWNLOAD)
    #关闭文件及Curl对象
    indexfile.close()
    c.close()

if __name__ == "__main__":
    url = sys.argv[1]
    main(url)
