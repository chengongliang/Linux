#!/bin/python

s = 'abcdefgh'
i = 0
s1 = ''

while i < len(s):
    s1 = s1 + (s[i:i+2])[::-1]
    i += 2
print s1
