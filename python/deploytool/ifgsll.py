#!/usr/bin/python
#coding:utf8

import os
import yaml
from optparse import OptionParser

cwd = os.getcwd()
def opt():
	parser = OptionParser()
	parser.add_option('-p','--porject',
					dest='project',
					action='store',
					help='project')
	parser.add_option('-l','--host',
					dest='host',
					action='store',
					help='host')
	parser.add_option('-c','--command',
					dest='command',
					action='store',
					help='command')
	options, args = parser.parse_args()
	return options, args

def parseHost(host, **args):
	hostcnf = os.path.join('%s' % cwd,'confs','server.yaml')
	hostinfo = yaml.load(file(hostcnf))
	for i in hostinfo:
		if host in i.split('-'):
			return hostinfo[i]['hostname'][:]

def parseProject(pro, **args):
	projCNF = os.path.join('%s' % cwd,'confs','projects','%s.yaml' % project)
	dirinfo = yaml.load(file(projCNF))
	return dirinfo

def backup():
	pass

def rollback():
	pass

def rsync(testServer,destDir,exclude):
	cmd = 'rsync -apv --delete --exclude={%s} %s:%s %s' % (exclude, testServer, destDir, destDir)
	os.system(cmd)

def getPID(project):
	cmd = "ps -ef|grep -v grep|grep %s|awk '{print $2}'" % project
	return os.system(cmd)

def startTomcat(project):
	binPath = os.join(destDir,"bin")
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

def update(hostname, project, exclude, destDir, tmpDir):
	#from salt.client import LocalClient
	#local = LocalClient()
	#print local.cmd(hostname, 'state.sls', [project])
	sync = 'rsync -ap --delete --exclude={%s} %s %s' % (exclude, destDir, tmpDir)
	os.system(sync)
	salt = 'salt "%s" state.sls %s' % (hostname, project)
	os.system(salt)

if __name__ == "__main__":
	options, args = opt()
	host = options.host
	project = options.project
	cmd = options.command
	dirinfo = parseProject(project)
	destDir = dirinfo[project]['dest'][:] 
	exclude = ','.join(dirinfo.get(project)['exclude'].split(' '))
	if cmd == 'rsync':
		if dirinfo.get(project)['type'] == 'www':
			testServer = '192.168.11.110'
			rsync(testServer, destDir, exclude)
		elif dirinfo.get(project)['type'] == 'tomcat':
			testServer = '192.168.11.110'
			rsync(testServer, destDir, exclude)
			stopTomcat(project)
			startTomcat(project)
	elif cmd == 'update':
		hostname = parseHost(host)
		tmpDir = dirinfo.get(project)['tmp']
		update(hostname, project, exclude, destDir, tmpDir)
