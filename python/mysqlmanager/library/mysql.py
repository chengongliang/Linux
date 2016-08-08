#!/usr/bin/python

import os
from ConfigParser import ConfigParser

class MySQLConfig(ConfigParser):
	def __init__(self, config, **kw):
		ConfigParser.__init__(self, allow_no_value=True)
		self.mysqld_vars = {}
		self.config = config
		if os.path.exists(self.config):
			self.read(self.config)
			self.get_mysqld_vars()
		else:
			self.get_defaults_mysqld_vars()
		self.set_mysqld_vars(kw)

	def set_mysqld_vars(self, kw):
		for k, v in kw.items():
			setattr(self,k,v)
			self.mysqld_vars[k] = v

	def set_vars(self, k, v):
		self.mysqld_vars[k] = v

	def get_mysqld_vars(self):
		rst = {}
		options = self.options('mysqld')
		for o in options:
			rst[o] = self.get('mysqld', o)
		self.set_mysqld_vars(rst)

	def get_defaults_mysqld_vars(self):
		defaults = {
			'port':'3306',
			'socket':'/tmp/mysql.sock',
			'skip-locking':None,
			'key_buffer_size':'16K',
			'max_allowed_packet':'1M',
			'table_open_cache':'4',
			'sort_buffer_size':'64K',
			'read_buffer_size':'256K',
			'read_rnd_buffer_size':'256K',
			'net_buffer_length':'2K',
			'thread_stack':'128K',
			}
		self.set_mysqld_vars(defaults)

	def save(self):
		if not self.has_section('mysqld'):
			self.add_section('mysqld')
		for k, v in self.mysqld_vars.items():
			self.set('mysqld', k, v)
		with open(self.config, 'w') as fd:
			self.write(fd)

if __name__ == '__main__':
	mc = MySQLConfig('/tmp/mysql.cnf', max_connections=200)
	mc.set_vars('skip-slave-start',None)
	mc.set_vars('port', 3306)
	mc.save()
	print mc.max_connections
	print mc.port
	print mc.socket
