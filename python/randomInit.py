#!/usr/bin/python
#coding:utf8

import random

number = random.randint(1,100)
guess = 0

while True:
    num_input = raw_input("please input one integer that is in 1 to 100: ")
    guess += 1

    if not num_input.isdigit():
        print "please input inerger."
    elif int(num_input) < 0 or int(num_input) >= 100:
        print "the number must be in 1 to 100"
        break
    else:
        if number == int(num_input):
            print "OK,you are right.\nguess time is %s" % guess
            break
        elif number > int(num_input):
            print "your number is smaller.\nguess time is %s" % guess
        elif number < int(num_input):
            print "your number is biger.\nguess time is %s" % guess
        else:
            print "There is something bad, I will not work"
