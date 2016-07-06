#!/usr/bin/python
#coding:utf8
def fib(n):
    result = [0,1]
    for i in range(n-2):
        result = result.append(result[-2]+result[-1])
    return result
if __name__ == "__main__":
    x = int(raw_input("请输入一个大等于2的数字："))
    print fib(x)
