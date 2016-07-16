#!/usr/bin/python
#coding:utf8

import os
import sys

if len(sys.argv) == 1:
    data = sys.stdin.read()
else:
    try:
        fn = sys.argv[1]
    except IndexError:
        print "please follow an argument at %s" % __file__
        sys.exit()
    if not os.path.exists(fn):
        print "%s is not exists" % fn
        sys.exit()
    fd = open(sys.argv[1])
    data = fd.read()
    fd.close()

chars = len(data)
words = len(data.split())
lines = data.count('\n')
print "%(lines)s %(words)s %(chars)s" % locals()
