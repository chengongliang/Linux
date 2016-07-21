#!/usr/bin/python
import os
from subprocess import Popen, PIPE

def getPid():
	p = Popen(['pidof','nginx'],stdout=PIPE,stderr=PIPE)
	pids = p.stdout.read().split()
	return pids

def parsePidFile(pids):
	sum = 0
	for i in pids:
		fn = os.path.join('/proc/',i,'status')
		with open(fn) as fd:
			for line in fd:
				if line.startswith('VmRSS'):
					mem = int(line.split()[1])
					sum += mem
					break
	return sum

def total_mem(f):
	with open(f) as fd:
		for line in fd:
			if line.startswith('MemTotal'):
				total_mem = int(line.split()[1])
				return total_mem

if __name__ == '__main__':
	pids = getPid()
	nginx_mem = parsePidFile(pids)
	total = total_mem('/proc/meminfo')
	print "Nginx memory is: %s KB" % nginx_mem
	print "Percent: %.2f%%" % (nginx_mem/float(total)*100)
