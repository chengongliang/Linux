#!/usr/bin/env python

import random
from vmconfig import readConfs
from subprocess import Popen, PIPE

XML = """<domain type='kvm' id='1'>
  <name>%(name)s</name>
  <uuid>%(uuid)s</uuid>
  <memory unit='KiB'>524288</memory>
  <currentMemory unit='KiB'>524288</currentMemory>
  <vcpu placement='static'>2</vcpu>
  <os>
    <type arch='x86_64' machine='rhel6.6.0'>hvm</type>
    <kernel>/tmp/vmlinuz</kernel>
    <initrd>/tmp/initrd.img</initrd>
    <cmdline>method=ftp://%(ftp_ip)s/pub ks=ftp://%(ftp_ip)s/ks/ks.cfg</cmdline>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <pae/>
  </features>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>destroy</on_reboot>
  <on_crash>destroy</on_crash>
  <devices>
    <emulator>/usr/libexec/qemu-kvm</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='raw' cache='none'/>
      <source file='%(disk)s'/>
      <target dev='vda' bus='virtio'/>
      <alias name='virtio-disk0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
    </disk>
    <controller type='usb' index='0' model='ich9-ehci1'>
      <alias name='usb0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x7'/>
    </controller>
    <controller type='usb' index='0' model='ich9-uhci1'>
      <alias name='usb0'/>
      <master startport='0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0' multifunction='on'/>
    </controller>
    <controller type='usb' index='0' model='ich9-uhci2'>
      <alias name='usb0'/>
      <master startport='2'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x1'/>
    </controller>
    <controller type='usb' index='0' model='ich9-uhci3'>
      <alias name='usb0'/>
      <master startport='4'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x2'/>
    </controller>
    <interface type='bridge'>
      <mac address='%(mac)s'/>
      <source bridge='br0'/>
      <target dev='vnet0'/>
      <model type='virtio'/>
      <alias name='net0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
    </interface>
    <serial type='pty'>
      <source path='/dev/pts/2'/>
      <target port='0'/>
      <alias name='serial0'/>
    </serial>
    <console type='pty' tty='/dev/pts/2'>
      <source path='/dev/pts/2'/>
      <target type='serial' port='0'/>
      <alias name='serial0'/>
    </console>
    <input type='tablet' bus='usb'>
      <alias name='input0'/>
    </input>
    <input type='mouse' bus='ps2'/>
    <graphics type='vnc' port='%(port)s' autoport='no' listen='0.0.0.0'>
      <listen type='address' address='0.0.0.0'/>
    </graphics>
    <video>
      <model type='cirrus' vram='9216' heads='1'/>
      <alias name='video0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
    </video>
    <memballoon model='virtio'>
      <alias name='balloon0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
    </memballoon>
  </devices>
</domain>
"""

def getUUID():
    p = Popen(['uuidgen'], stdout=PIPE)
    uuid = p.stdout.read().strip()
    return {'uuid': uuid}

def getIP():
    #ftp_ip
    #p = Popen(['ifconfig', 'br0'], stdout=PIPE)
    #data = p.stdout.read()
    #ip = data.split('\n')[1].split()[1].split(':')[1]
    return {'ftp_ip': '192.168.11.210'}

def getMAC():
    hex = '0123456789abcde'
    mac = "00:0C:29:%s%s:%s%s:%s%s" % tuple([random.choice(hex) for i in range(6)])
    return {'mac': mac}

def getPort():
    ports = []
    vm_msg = readConfs()
    if vm_msg:
        for i in vm_msg:
            port = i.values()[0]['port']
            ports.append(port)
        ports.sort()
        new_port = int(ports[-1]) + 1
    else:
        new_port = 5901
    return {'port': new_port}

if __name__ == '__main__':
    print getUUID()
    print getIP()
    print getMAC()
    print getPort()
