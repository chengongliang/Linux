#!/usr/bin/python

from subprocess import Popen, PIPE

def getIP():
    p = Popen(['ifconfig'],stdout=PIPE)
    data = p.stdout.read().split('\n\n')
    
