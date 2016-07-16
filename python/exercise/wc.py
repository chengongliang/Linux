#!/usr/bin/python
#coding:utf8

import sys

fd = open(sys.argv[1])
data = fd.read()
chars = len(data)
words = len(data.split())
lines = data.count('\n')

print lines,chars,words
