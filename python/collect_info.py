#!/usr/bin/python

from subprocess import Popen, PIPE

def getHostname(f):
	with open(f) as fd:
		for line in fd:
			if line.startswith('HOSTNAME'):
				hostname = line.split('=')[1].strip()
				break
	return {'Hostname':hostname}

def getOSver(f):
	with open(f) as fd:
		for line in fd:
			osver = line.strip()
			break
	return {'OSversion':osver}

def getCPU(f):
	num = 0
	with open(f) as fd:
		for line in fd:
			if line.startswith('processor'):
				num += 1
			if line.startswith('model name'):
				cpu_model = line.split(':')[1].split()
				cpu_model = cpu_model[0]+' '+cpu_model[3]+' '+cpu_model[-1]
		return {'cpu_num':num, 'cpu_model':cpu_model}

def getMemory(f):
	with open(f) as fd:
		for line in fd:
			if line.startswith('MemTotal'):
				mem = int(line.split()[1].strip())
				break
	mem = "%s" % (mem/1024.0)+'M'
	return {'memory':mem}

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
	dic = {}
	data_ip = getIP()
	parsed_data_ip = parseData(data_ip)
	ip = parseIfconfig(parsed_data_ip)
	data_dmi = getDmi()
	parsed_data_dmi = parseData(data_dmi)
	dmi = parseDmi(parsed_data_dmi)
	hostname = getHostname('/etc/sysconfig/network')
	osver = getOSver('/etc/issue')
	cpu = getCPU('/proc/cpuinfo')
	mem = getMemory('/proc/meminfo')
	dic.update(ip)
	dic.update(dmi)
	dic.update(cpu)
	dic.update(mem)
	dic.update(hostname)
	dic.update(osver)
	print dic
