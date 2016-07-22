#!/usr/bin/python

from subprocess import Popen, PIPE

def getIP():
    p = Popen(['ifconfig'],stdout=PIPE)
    stdout, stderr = p.communicate()
    data = [i for i in stdout.split('\n') if i and not i.startswith('lo')]
    return data
    
def genIP():
    new_line = ''
    lines = []
    for line in data:
        if line[0].strip():
            lines.append(new_line)
            new_line = line + '\n'
        else:
            new_line = line + '\n'
    lines.append(new_line)
    return [i for i in lines if i]
    
def parseIP(data):
    dic = {}
    for lines in data:
        line_list = lines_split('\n')
        devname = line_list[0].split()[0]
        macaddr = line_list[0].split()[-1]
        ipaddr = line_list[1].split()[1].split(':')[1]
        dic[devname] = [macaddr, ipaddr]
    return dic

if __name__ == '__main__':
    data = getIP()
    data_list = genIP(data)
    print parseIP(data_list)
