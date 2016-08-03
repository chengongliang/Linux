#!/usr/bin/python
#coding:utf8
import paramiko
import multiprocessing
import sys
from optparse import OptionParser

def opt():
	parser = OptionParser("Usage: %prog -a <address> command")
	parser.add_option('-a',
					dest='addr',
					action='store',
					help='ip or iprange EX:192.168.1,192.168.1.2 or 192.168.1.1-192.168.1.100')
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
		print "%s:\t %s" % (ip, stdout)
		ssh.close()
	else:
		print "%s:\t %s" % (ip, stderr)
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
	else:
		print "%s -h" %__file__
		sys.exit(1)
	pool = multiprocessing.Pool(processes=10)
	for ip in ips:
		pool.apply_async(func=ssh_conn, args=(ip, cmd))
	pool.close()
	pool.join()
