#!/usr/bin/python
#coding:utf-8
import random

score = [random.randint(1,100) for i in range(30)]
print score

sum_score = sum(score)
num = len(score)
ave_score = sum_score/num
print "The avarge score is %s." % ave_score

less_num = len([i for i in score if i < ave_score])
print "There are %s students less than average score." % less_num

sort_score = sorted(score,reverse=False)
print sort_score
