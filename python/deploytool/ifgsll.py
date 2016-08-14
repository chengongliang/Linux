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
	else:
		print "ip或者hostname未写入配置"
		sys.exit(1)

def parseProject(project, **args):
	projCNF = os.path.join('%s' % cwd,'confs','projects','%s.yaml' % project)
	if not os.path.exists(projCNF):
		print "%s 不存在或未配置" % project
		sys.exit(1)
	dirinfo = yaml.load(file(projCNF))
	return dirinfo

class BR:
	def __init__(self, project, destDir, **kw):
		import datetime
		today = datetime.date.today()
		BACK_DIR = "/home/ifgsll/backup/"
		self.backDir = BACK_DIR + today.isoformat()
		self.p_back = self.backDir + '/' + destDir.split('/')[-2] + '/'

	def backup(self, project, destDir, exclude):
		if not os.path.exists(self.backDir):
			os.makedirs(self.backDir)
		rsync = "rsync -avp --delete --exclude={%s} %s %s" % (exclude, destDir, self.p_back)
		os.system(rsync)
		
	def rollback(self, project, destDir, exclude):
		rsync = "rsync -avp --delete --exclude={%s} %s %s" % (exclude, self.p_back, destDir)
		os.system(rsync)

def rsync(testServer,destDir,exclude):
	cmd = 'rsync -apv --delete --exclude={%s} %s:%s %s' % (exclude, testServer, destDir, destDir)
	if not os.path.exists(destDir):
		os.makedirs(destDir)
	os.system(cmd)

def getPID(host, project):
	from subprocess import Popen, PIPE
	salt_cmd = "salt '%s' cmd.run 'ps -ef|grep -v grep|grep %s'" % (host,project)
	p = Popen(salt_cmd, stdout=PIPE, stderr=PIPE, shell=True)
	stdout, stderr = p.communicate()
	if stderr.split(': ')[0] != 'ERROR':
		pid = stdout.split('\n')[1].strip().split(' ')[6]
		return pid
	else:
		print "程序未运行。"
		sys.exit(1)

def startTomcat(hostname, destDir):
	binPath = destDir + "bin"
	cmd = "sh %s/startup.sh" % binPath
	cmd_run = "salt '%s' cmd.run '%s'" % (hostname, cmd)
	project = destDir.split('/')[-2]
	try:
		os.system(cmd_run)
		print "%s 已经启动" % project
	except OSError, e:
		print"启动失败!"

def stopTomcat(hostname, destDir):
	pid = getPID(hostname, destDir)
	cmd = "salt '%s' cmd.run 'kill -9 %s'" % (hostname, pid)
	os.system(cmd)
	project = destDir.split('/')[-2]
	try:
		print "%s 的进程已停止,PID: %s" % (project, pid)
	except OSError, e:
		print "%s 停止失败" % project

def update(hostname, project, exclude, destDir, tmpDir, env):
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
		br = BR(project, destDir)
		testServer = '192.168.11.110'
		if env == 'www':
			rsync(testServer, destDir, exclude)
		elif env == 'tomcat':
			rsync(testServer, destDir, exclude)
		br.backup(project, destDir)
	elif cmd == 'update':
		hostname = parseHost(host)
		tmpDir = dirinfo.get(project)['tmp']
		update(hostname, project, exclude, destDir, tmpDir, env)
	elif cmd == 'rollback':
		br = BR(project, destDir)
		br.rollback(project, destDir)
	elif cmd == 'stop':
		if env == 'tomcat':
			hostname = parseHost(host)
			stopTomcat(hostname, destDir)
	elif cmd == 'start':
		if env == 'tomcat':
			hostname = parseHost(host)
			startTomcat(hostname, destDir)
	elif cmd == 'restart':
		if env == 'tomcat':
			hostname = parseHost(host)
			stopTomcat(hostname, destDir)
			startTomcat(hostname, destDir)
	else:
		print "未知命令!\n请使用 %s -h 查看帮助信息" % __file__
		sys.exit(1)
