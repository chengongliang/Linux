#!/usr/bin/python
#coding:utf8

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
            ##移除字符串的空格和tab
                lines.append(line)
            else:
                break
    return lines
   
def dmiDic():
    dmi_dic = {}
    data = getDmi()
    lines = parseDmi(data)
    dic = dict([i.strip().split(': ') for i in lines]
    dmi_dic['vendor'] = dic['Manufacturer']
    dmi_dic['profuct'] = dic['Product Name']
    dmi_dic['sn'] = dic['Serial Number']
    return dmi_dic
 
if __name__ == '__main__':
    print dmiDic()
