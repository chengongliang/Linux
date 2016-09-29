#!/usr/bin/env python
#coding:utf8
#author:chengongliang
import sys
import MySQLdb

class mySQL():

    def __init__(self):
        try:
            self.conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='jandan',port=3306)
            self.cur = self.conn.cursor()
        except MySQLdb.Error,e:
            print "MySQL error %d:%s" % (e.args[0],e.args[1])
            sys.exit(1)

    def get_agent(self):
        self.cur.execute("select info from configs where config='agent'")
        sql_data = self.cur.fetchall()
        List = sql_data[0][0].split("','")
        return List

    def get_num(self):
        self.cur.execute("select info from configs where config='page_num'")
        num = self.cur.fetchall()[0][0]
        return num

    def put_num(self,conf,num):
        self.cur.execute("UPDATE `jandan`.`configs` SET `info`=%s WHERE (`config`=%s)",[num, conf])
        self.conn.commit()
        #self.close()

    def put_ooxx(self,url,oo,xx):
        self.cur.execute("INSERT INTO `jandan`.`ooxx` (`url`, `oo`, `xx`) SELECT %s, %s, %s FROM dual WHERE NOT EXISTS (SELECT url FROM ooxx WHERE url = %s)",[url,oo,xx,url])
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

#if __name__ == '__main__':
#    s = mySQL()
#    l = s.get_agent()
#    num = s.get_num()
#    print num
#    print l[0]
#    print "_*" * 20
#    print l[1]
#    print "_*" * 20
#    s.put_num('page_num','2017')
    #s.close()
