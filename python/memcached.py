#!/usr/bin/env python
#coding:utf8
import sys
import os
from subprocess import Popen, PIPE

class Process(object):
    '''memcached rc script'''
    def __init__(self,name,program,args,workdir):
        self.name = name
        self.program = program
        self.args = args
        self.workdir = workdir

    def _init(self):
        '''/var/tmp/memcached'''
        if not os.path.exists(self.workdir):
            os.mkdir(self.workdir)
            os.chdir(self.workdir)

    def _pidFile(self):
        '''/var/tmp/memcached/memcached.pid'''
        return os.path.join(self.workdir, "%s.pid" % self.name)

    def _getPid(self):
        p = Popen(['pidof',self.name], stdout=PIPE)
        pid = p.stdout.read().strip()
        return pid

    def _writePid(self):
        if self.pid:
            with open(self._pidFile(), 'w') as fd:
                fd.write(str(self.pid))

    def start(self):
        pid = self._getPid()
        if pid:
            print "%s is running..." % self.name
            sys.exit() 
        self._init()
        cmd = self.program + ' ' + self.args
        p = Popen(cmd, stdout=PIPE, shell=True)
        self.pid = p.pid
        self._writePid()
        print "%s start successful" % self.name

    def stop(self):
        pid = self._getPid()
        if pid:
            os.kill(int(pid), 15)
            if os.path.exists(self._pidFile()):
                os.remove(self._pidFile())
            print "%s is stopped" % self.name

    def restart(self):
        self.stop()
        self.start()

    def status(self):
        pid = self._getPid()
        if pid:
            print "%s is already running" % self.name
        else:
            print "%s is not running" % self.name
    def help(self):
        print "Usage: %s {start|stop|restart|status}" % __file__

def main():
    name = 'memcached'
    prog = '/usr/bin/memcached'
    args = '-u nobody -p 11211 -c 1024 -m 64'
    wdir = '/var/tmp/memcached'
    pm = Process(name = name,
                program = prog,
                args = args,
                workdir = wdir
                )
    try:
        cmd = sys.argv[1]
    except IndexError, e:
        print "Option error"
        sys.exit()
    if cmd == 'start':
        pm.start()
    elif cmd == 'stop':
        pm.stop()
    elif cmd == 'status':
        pm.status()
    elif cmd == 'restart':
        pm.restart()
    else:
        pm.help()

if __name__== '__main__':
    main()
