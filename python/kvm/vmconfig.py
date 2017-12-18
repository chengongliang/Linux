#!/usr/bin/env python

import re


def match(s):
    re_name = re.compile(r"<name>(.*)</name>")
    re_disk = re.compile(r"<source file='(.*)'/>")
    re_mac = re.compile(r"<mac address='(.*)'/>")
    re_port = re.compile(r"<graphics type='vnc' port='(\d+)'")

    vm_name = re_name.search(s)
    vm_disk = re_disk.search(s)
    vm_mac = re_mac.search(s)
    vm_port = re_port.search(s)

    if vm_name:
        return {'name': vm_name.group(1)}
    elif vm_disk:
        return {'disk': vm_disk.group(1)}
    elif vm_mac:
        return {'mac': vm_mac.group(1)}
    elif vm_port:
        return {'port': vm_port.group(1)}


def readConfs():
    import glob
    confs = glob.glob('/etc/libvirt/qemu/*.xml')
    values = []
    for conf in confs:
        dic = {}
        with open(conf) as fd:
            for line in fd:
                if match(line):
                    dic.update(match(line))
        dic_tmp = {dic.pop('name'): dic}
        values.append(dic_tmp)
    return values


if __name__ == "__main__":
    print readConfs()
