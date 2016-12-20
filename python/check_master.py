#!/usr/bin/env python
#_*_coding:utf8_*_
'''
nagios 报警插件：
根据哨兵提供的信息，检查对应 ip port 是否为 master 节点
'''
import sys
import redis

server ={
       26379:'test01',
       26380:'test02',
       26381:'test03',
       26382:'test04',
       26383:'test05',
       26384:'test06'
   }

def check_sentinel(s_port,name):
    r = redis.Redis(host='10.0.10.1',port=s_port)
    return r.sentinel_get_master_addr_by_name(name)

def check_master(_host,r_port):
    r = redis.Redis(host=_host,port=r_port)
    return r.info()['role']

if __name__ == "__main__":
    master_list = []
    for s_port in server:
        name = server[s_port]
        #print name,s_port
        host,r_port = check_sentinel(s_port,name)
        #print host,r_port
        if check_master(host,r_port) == "master":
            master_list.append(host+':'+str(r_port))
        else:
            print "CRITICAL: %s:%s not a master,check 10.0.10.1 Sentinel: %s" %(host,r_port,s_port)
            sys.exit(2)
    print "OK: master list is %s" %master_list
