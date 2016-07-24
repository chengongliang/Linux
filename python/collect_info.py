#!/usr/bin/python
#coding:utf8

from subprocess import Popen, PIPE

def getIP():
	p = Popen(['ifconfig'],stdout=PIPE)
	data = p.stdout.read()
	return data

def getDmi():
	p = Popen(['dmidecode'],stdout=PIPE)
	data = p.stdout.read()
	return data

def parseData(data):
	parsed_data = []
	new_line = ''
	data = [i for i in data.split('\n') if i]
	for line in data:
		if line[0].strip():
			parsed_data.append(new_line)
			new_line = line+'\n'
		else:
			new_line += line+'\n'
	parsed_data.append(new_line)
	return [i for i in parsed_data if i]

def parseIfconfig(parsed_data):
	dic = {}
	parsed_data = [i for i in parsed_data if not i.startswith('lo')]
	for lines in parsed_data:
		line_list = lines.split('\n')
		devname = line_list[0].split()[0]
		macaddr = line_list[0].split()[-1]
		ipaddr = line_list[1].split()[1].split(':')[1]
		break
	dic['IP'] = ipaddr
	return dic

def parseDmi(parsed_data):
	dic = {}
	parsed_data = [i for i in parsed_data if i.startswith('System Information')]
	parsed_data = parsed_data[0].split('\n')[1:]
	dmi_dic = dict([i.strip().split(':') for i in parsed_data if i])
	dic['vendor'] = dmi_dic['Manufacturer']
	dic['product'] = dmi_dic['Product Name']
	dic['sn'] = dmi_dic['Serial Number']
	return dic

if __name__ == '__main__':
	data_ip = getIP()
	parsed_data_ip = parseData(data_ip)
	print parseIfconfig(parsed_data_ip)
	data_dmi = getDmi()
	parsed_data_dmi = parseData(data_dmi)
	print parseDmi(parsed_data_dmi)
