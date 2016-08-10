#!/usr/bin/python

import os
import sys
import time
import MySQLdb
import shlex
from optparse import OptionParser
from subprocess import Popen, PIPE

DIRNAME = os.path.dirname(__file__)
OPSTOOL = os.path.abspath(os.path.join(DIRNAME, '..'))
sys.path.append(OPSTOOL)

from library.mysql import MySQLConfig

MYSQL_DATA_DIR = '/var/mysqlmanager/data'
MYSQL_CONF_DIR = '/var/mysqlmanager/conf'
def opt():
	parser = OptionParser()
	parser.add_option('-n', '--name',
					dest='name',
					action='store',
					default='myinstance',
					help='NAME')
	parser.add_option('-p', '--port',
					dest='port',
					action='store',
					default='3306',
					help='PORT')
	parser.add_option('-c', '--command',
					dest='command',
					action='store',
					default='check',
					help='NAME')
	options, args = parser.parse_args()
	return options, args

def _init():
	if not os.path.exists(MYSQL_DATA_DIR):
		os.makedirs(MYSQL_DATA_DIR)
	if not os.path.exists(MYSQL_CONF_DIR):
		os.makedirs(MYSQL_CONF_DIR)

def readConfs():
	import glob
	confs = glob.glob(MYSQL_CONF_DIR+'/*.cnf')
	return confs

def checkPort(conf_file, port):
	mc = MySQLConfig(conf_file)
	if mc.mysqld_vars['port'] == port:
		return True
	else:
		return False

def _genDict(name, port):
	return{
		'pid-file': os.path.join(MYSQL_DATA_DIR,name,'%s.pid' % name),
		'socket': '/tmp/%s.sock' % name,
		'port': port,
		'datadir': os.path.join(MYSQL_DATA_DIR,name),
		'log-error': os.path.join(MYSQL_DATA_DIR,name,'%s.log' % name)
		}

def getCNF(name):
	cnf = os.path.join(MYSQL_CONF_DIR, '%s.cnf' % name)
	return cnf

def mysql_install(name):
	cnf = getCNF(name)
	cmd = "mysql_install_db --defaults-file=%s" % cnf
	p = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
	p.communicate()
	p.returncode

def setOwner(datadir):
	os.system('chown -R mysql:mysql %s' % datadir)

def mysql_run(name):
	cnf = getCNF(name)
	cmd = "mysqld_safe --defaults-file=%s &" % cnf
	p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
	time.sleep(2)
	p.returncode

def createInstance(name, port):
	exists_confs = readConfs()
	for conf in exists_confs:
		if conf.split('/')[-1][:-4] == name:
			print >> sys.stderr, "Instance: %s is exists" % name
			sys.exit(-1)
		if checkPort(conf, port):
			print >> sys.stderr, "Port: %s is exists" % name
			sys.exit(-1)
	cnf = getCNF(name)
	if not os.path.exists(cnf):
		c = _genDict(name, port)
		mc = MySQLConfig(cnf, **c)
		mc.save()
	datadir = os.path.join(MYSQL_DATA_DIR,name)
	if not os.path.exists(datadir):
		mysql_install(name)
		setOwner(datadir)
		mysql_run(name)

def connMysql(name):
	cnf = getCNF(name)
	if os.path.exists(cnf):
		mc = MySQLConfig(cnf)
		port = int(mc.mysqld_vars['port'])
		host = '127.0.0.1'
		user = 'root'
		conn = MySQLdb.connect(host=host, port=port, user=user)
		cur = conn.curson()
		return cur

def getMyVariables(cur):
	sql = "show global variables"
	cur.execute(sql)
	data = cur.fetchall()
	return data

def diffMyVariables(name):
	cur = connMysql(name)
	vars = getMyVariables(cur)
	cnf = getCNF(name)
	mc = MySQLConfig(cnf)
	for k, v in mc.mysqld_vars.items():
		k = k.replace('-','_')
		if k in vars and v != vars[k]:
			print k, v, vars[k]

if __name__ == "__main__":
	_init()
	options, args = opt()
	instance_name = options.name
	instance_port = options.port
	instance_cmd = options.command
	if instance_cmd == 'create':
		createInstance(instance_name, instance_port)
	elif instance_cmd == 'check':
		diffMyVariables(instance_name)
#!/usr/bin/python

import os
import sys
import time
import MySQLdb
import shlex
from optparse import OptionParser
from subprocess import Popen, PIPE

DIRNAME = os.path.dirname(__file__)
OPSTOOL = os.path.abspath(os.path.join(DIRNAME, '..'))
sys.path.append(OPSTOOL)

from library.mysql import MySQLConfig

MYSQL_DATA_DIR = '/var/mysqlmanager/data'
MYSQL_CONF_DIR = '/var/mysqlmanager/conf'
def opt():
	parser = OptionParser()
	parser.add_option('-n', '--name',
					dest='name',
					action='store',
					default='myinstance',
					help='NAME')
	parser.add_option('-p', '--port',
					dest='port',
					action='store',
					default='3306',
					help='PORT')
	parser.add_option('-c', '--command',
					dest='command',
					action='store',
					default='check',
					help='NAME')
	options, args = parser.parse_args()
	return options, args

def _init():
	if not os.path.exists(MYSQL_DATA_DIR):
		os.makedirs(MYSQL_DATA_DIR)
	if not os.path.exists(MYSQL_CONF_DIR):
		os.makedirs(MYSQL_CONF_DIR)

def readConfs():
	import glob
	confs = glob.glob(MYSQL_CONF_DIR+'/*.cnf')
	return confs

def checkPort(conf_file, port):
	mc = MySQLConfig(conf_file)
	if mc.mysqld_vars['port'] == port:
		return True
	else:
		return False

def _genDict(name, port):
	return{
		'pid-file': os.path.join(MYSQL_DATA_DIR,name,'%s.pid' % name),
		'socket': '/tmp/%s.sock' % name,
		'port': port,
		'datadir': os.path.join(MYSQL_DATA_DIR,name),
		'log-error': os.path.join(MYSQL_DATA_DIR,name,'%s.log' % name)
		}

def getCNF(name):
	cnf = os.path.join(MYSQL_CONF_DIR, '%s.cnf' % name)
	return cnf

def mysql_install(name):
	cnf = getCNF(name)
	cmd = "mysql_install_db --defaults-file=%s" % cnf
	p = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
	p.communicate()
	p.returncode

def setOwner(datadir):
	os.system('chown -R mysql:mysql %s' % datadir)

def mysql_run(name):
	cnf = getCNF(name)
	cmd = "mysqld_safe --defaults-file=%s &" % cnf
	p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
	time.sleep(2)
	p.returncode

def createInstance(name, port):
	exists_confs = readConfs()
	for conf in exists_confs:
		if conf.split('/')[-1][:-4] == name:
			print >> sys.stderr, "Instance: %s is exists" % name
			sys.exit(-1)
		if checkPort(conf, port):
			print >> sys.stderr, "Port: %s is exists" % name
			sys.exit(-1)
	cnf = getCNF(name)
	if not os.path.exists(cnf):
		c = _genDict(name, port)
		mc = MySQLConfig(cnf, **c)
		mc.save()
	datadir = os.path.join(MYSQL_DATA_DIR,name)
	if not os.path.exists(datadir):
		mysql_install(name)
		setOwner(datadir)
		mysql_run(name)

def connMysql(name):
	cnf = getCNF(name)
	if os.path.exists(cnf):
		mc = MySQLConfig(cnf)
		port = int(mc.mysqld_vars['port'])
		host = '127.0.0.1'
		user = 'root'
		conn = MySQLdb.connect(host=host, port=port, user=user)
		cur = conn.curson()
		return cur

def getMyVariables(cur):
	sql = "show global variables"
	cur.execute(sql)
	data = cur.fetchall()
	return data

def diffMyVariables(name):
	cur = connMysql(name)
	vars = getMyVariables(cur)
	cnf = getCNF(name)
	mc = MySQLConfig(cnf)
	for k, v in mc.mysqld_vars.items():
		k = k.replace('-','_')
		if k in vars and v != vars[k]:
			print k, v, vars[k]

if __name__ == "__main__":
	_init()
	options, args = opt()
	instance_name = options.name
	instance_port = options.port
	instance_cmd = options.command
	if instance_cmd == 'create':
		createInstance(instance_name, instance_port)
	elif instance_cmd == 'check':
		diffMyVariables(instance_name)
