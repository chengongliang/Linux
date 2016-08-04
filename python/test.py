#!/usr/bin/python
#coding:utf8
import paramiko
import multiprocessing
import json
import sys
import urllib, urllib2
from optparse import OptionParser

DATA_BACK = '/var/tmp/data.json'
def opt():
	parser = OptionParser("Usage: %prog -a <address>/or -g <groupname> command")
	parser.add_option('-a',
					dest='addr',
					action='store',
					help='ip or iprange EX:192.168.1.11,192.168.1.12 or 192.168.1.2-192.168.1.100')
	parser.add_option('-g',
					dest='group',
					action='store',
					help='groupname')
	options, args = parser.parse_args()
	return options, args

def ssh_conn(ip, cmd):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	pkey_file = '/root/.ssh/id_rsa'
	key = paramiko.RSAKey.from_private_key_file(pkey_file)
	try:
		ssh.connect(hostname=ip, username='root',pkey=key, timeout=5)
	except:
		print "%s: Timeout or not permission" % ip
		return 1
	stdin, stdout, stderr = ssh.exec_command(cmd)
	stdout = stdout.read()[:-1]
	stderr = stderr.read()[:-1]
	if stdout:
		print "%s:\t%s" % (str(ip), stdout)
		ssh.close()
	else:
		print "%s:\t %s" % (str(ip), stderr)
        ssh.close()

def parseOpt(option):
	if ',' in option:
		ips = option.split(',')
		return ips
	elif '-' in option:
		ip_start, ip_end = option.split('-')
		ip_net = '.'.join(ip_start.split('.')[:-1])
		start = int(ip_start.split('.')[-1])
		end = int(ip_end.split('.')[-1]) + 1
		ips = [ip_net+'.'+str(i) for i in range(start, end)]
		return ips
	elif ',' not in option or '-' not in option:
		ips = [option]
		return ips
	else:
		print "%s -a <address> command" % __file__

def getData():
	url = 'http://192.168.11.210:8000/hostinfo/getjson/'
	try:
		req = urllib2.urlopen(url)
		data = json.loads(req.read())
		with open(DATA_BACK, 'wb') as fd:
			json.dump(data, fd)
	except:
		with open(DATA_BACK) as fd:
			data = json.load(fd)
	return data

def parseData(data):
	dic_host = {}
	for hg in data:
		groupname = hg['groupname']
		dic_host[groupname] = []
		for h in hg['members']:
			dic_host[groupname] += [h['ip']]
	return dic_host

if __name__ == "__main__":
	paramiko.util.log_to_file('/tmp/paramiko.log')
	options, args = opt()
	try:
		cmd = args[0]
	except IndexError:
		print "%s -a <address> command" % __file__
		sys.exit(1)
	if options.addr:
		ips = parseOpt(options.addr)
	elif options.group:
		groupname = options.group
		data = getData()
		dic = parseData(data)
		if groupname in dic:
			ips = dic[groupname]
		else:
			print "%s is not exists in SimpleCMDB" % groupname
	else:
		print "%s -h" %__file__
		sys.exit(1)
	pool = multiprocessing.Pool(processes=5)
	for ip in ips:
		pool.apply_async(func=ssh_conn, args=(ip, cmd))
	pool.close()
	pool.join()
