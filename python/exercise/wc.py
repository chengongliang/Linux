#!/usr/bin/python
#coding:utf8

import sys

data = sys.stdin.read()

chars = len(data)
words = len(data.split())
lines = data.count('\n')

print lines,chars,words
