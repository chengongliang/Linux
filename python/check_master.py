#!/usr/bin/env python
# _*_coding:utf8_*_
'''
nagios 报警插件：
根据哨兵提供的信息，检查对应 ip port 是否为 master 节点
'''
import sys
import redis
import commands

bond0 = commands.getoutput('ifconfig bond0')
host = bond0.split('\n')[1].strip().split(' ')[1].split(':')[1]

server = {
    26379: 'car01',
    26380: 'car02',
    # 26382:'attendance',
    # 26383:'statistic',
    26384: 'activity'
}


def check_sentinel(s_port, name):
    try:
        r = redis.Redis(host=host, port=s_port)
        return r.sentinel_get_master_addr_by_name(name)
    except redis.exceptions.ConnectionError, e:
        print "CRITICAL: %s" % e
        sys.exit(2)


def check_master(_host, r_port):
    try:
        r = redis.Redis(host=_host, port=r_port)
        info = r.info()
        return info['connected_slaves'], info['role']
    except redis.exceptions.ConnectionError, e:
        print "CRITICAL: %s" % e
        sys.exit(2)


if __name__ == "__main__":
    master_list = []
    for s_port in server:
        name = server[s_port]
        host, r_port = check_sentinel(s_port, name)
        slaves_num, role = check_master(host, r_port)
        if slaves_num != 2:
            print "CRITICAL: %s:%s connected_slaves %s" % (host, r_port, slaves_num)
            sys.exit(2)
        if role == "master":
            master_list.append(host + ':' + str(r_port) +
                               ' slaves_num: ' + str(slaves_num))
        else:
            print "CRITICAL: %s:%s not a master,check %s Sentinel: %s" % (host, r_port, host, s_port)
            sys.exit(2)
    print "OK: master list is %s" % master_list
