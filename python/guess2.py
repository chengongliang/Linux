#!/usr/bin/python

import random
import sys

r_num=random.randint(0,20)
for i in xrange(1,7):
    i_num = input ("please input a number:")
    if type(i_num) == int:
        pass
    else:
        print "please input a integer number!"
        break
    if i_num == r_num:
        print "congratulation,you are succeed!"
        print "guess times %s" %i
        sys.exit()
    if i_num > r_num:
        print "too big!"
        print "error times %s" %i
        continue
    if i_num < r_num:
        print "too small!"
        print "error times %s" %i
        continue
    else:
        print "You are wrong , please try again!"
        print "error times %s" %i
        continue
print "the result is %s" %r_num
