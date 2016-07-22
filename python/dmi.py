#!/usr/bin/python

from subprocess import Popen, PIPE

def getDmi():
    p = Popen(['dmidecode'],stdout=PIPE)
    data = p.stdout.read()
    return data
    
def parseDmi():
    lines = []
    line_in = False
    dmi_list = [i for i in data.split('\n') if i]
    ## if i --只取非空值
    for line in dmi_list:
        if line.startswith('System Information'):
        ## startswith('') 匹配行首内容
            line_in = True
            continue
        if line_in:
            if not line[0].strip():
            ##移除第一个字符为空格或tab，not转换为True
                lines.append(line)
            else:
                break
    return lines
    
if __name__ == '__main__':
    data = getDmi()
    print parseDmi(data)
