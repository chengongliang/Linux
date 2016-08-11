#!/usr/bin/python
#coding:utf8

import os
import sys
import yaml
from optparse import OptionParser

cwd = os.getcwd()
def opt():
	parser = OptionParser()
	parser.add_option('-p','--porject',
					dest='project',
					action='store',
					help='order,temorder')
	parser.add_option('-l','--host',
					dest='host',
					action='store',
					help='host')
	parser.add_option('-c','--command',
					dest='command',
					action='store',
					help='rsync,update,rollback,start,stop,restart')
	options, args = parser.parse_args()
	return options, args

def parseHost(host, **args):
	hostcnf = os.path.join('%s' % cwd,'confs','server.yaml')
	hostinfo = yaml.load(file(hostcnf))
	for i in hostinfo:
		if host in i.split('-'):
			return hostinfo[i]['hostname'][:]

def parseProject(project, **args):
	projCNF = os.path.join('%s' % cwd,'confs','projects','%s.yaml' % project)
	if not os.path.exists(projCNF):
		print "%s 不存在" % project
		sys.exit(1)
	dirinfo = yaml.load(file(projCNF))
	return dirinfo

def backup(project, destDir):
	import datetime
	today = datetime.date.today()
	BACK_DIR = "/home/ifgsll/backup/"
	backDir = BACK_DIR + today.isoformat()
	if not os.path.exists(backDir):
		os.makedirs(backDir)
	cmd = "cp -rf %s %s" % (destDir, backDir)
	os.system(cmd)

def rollback():
	pass

def rsync(testServer,destDir,exclude):
	cmd = 'rsync -apv --delete --exclude={%s} %s:%s %s' % (exclude, testServer, destDir, destDir)
	if not os.path.exists(destDir):
		os.makedirs(destDir)
	os.system(cmd)

def getPID(project):
	cmd = "ps -ef|grep -v grep|grep %s|awk '{print $2}'" % project
	return os.system(cmd)

def startTomcat(project):
	binPath = destDir + "bin"
	cmd = "cd %s && ./startup.sh" % binPath
	try:
		os.system(cmd)
		print "%s 已经启动" % project
	except OSError, e:
		print"启动失败!"

def stopTomcat(project):
	import signal
	pid = getPID(project)
	try:
		a = os.kill(pid, signal.SIGKILL)
		print "%s 的进程已停止,PID: %s, 返回值: %s" % (project, pid, a)
	except OSError, e:
		print "%s 没有运行" % project

def update(hostname, project, exclude, destDir, tmpDir, env):
	#from salt.client import LocalClient
	#local = LocalClient()
	#print local.cmd(hostname, 'state.sls', [project])
	sync = 'rsync -ap --delete --exclude={%s} %s %s' % (exclude, destDir, tmpDir)
	if not os.path.exists(tmpDir):
		os.makedirs(tmpDir)
	os.system(sync)
	salt = 'salt "%s" state.sls %s %s' % (hostname, project, env)
	os.system(salt)

if __name__ == "__main__":
	options, args = opt()
	host = options.host
	project = options.project
	cmd = options.command
	dirinfo = parseProject(project)
	env = dirinfo.get(project)['type']
	destDir = dirinfo[project]['dest'][:] 
	exclude = ','.join(dirinfo.get(project)['exclude'].split(' '))
	if cmd == 'rsync':
		if env == 'www':
			testServer = '192.168.11.110'
			rsync(testServer, destDir, exclude)
			backup(project, destDir)
		elif env == 'tomcat':
			testServer = '192.168.11.110'
			rsync(testServer, destDir, exclude)
		#	stopTomcat(project)
		#	startTomcat(project)
	elif cmd == 'update':
		hostname = parseHost(host)
		tmpDir = dirinfo.get(project)['tmp']
		update(hostname, project, exclude, destDir, tmpDir, env)
	else:
		print "command %s not support!\nPlease use %s -h to show helpinfo." % (cmd, __file__)
		sys.exit(1)
