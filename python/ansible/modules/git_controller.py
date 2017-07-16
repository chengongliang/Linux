#!/usr/bin/python
# _*_ coding:utf-8 _*_
import commands
import shlex
import os
import sys
import json


args_file = sys.argv[1]
args_data = file(args_file).read()


arguments = shlex.split(args_data)
key = ""
repo = ""
dest = ""
for arg in arguments:
    if "=" in arg:
        key, value = arg.split("=")
        if key == "tag":
            tag = value
        if key == "repo":
            repo = value
        if key == "dest":
            dest = value
    else:
        print json.dumps({"failed": True, "msg": "-a 'tag=xx repo=xx dest=xx'"})
        sys.exit(1)
if tag and repo and dest:
    if not os.path.isdir(dest):
        os.mkdir(dest)
    os.chdir(dest)
    data = commands.getstatusoutput("git remote -v")
    if data[0] != 0:
        print json.dumps({"failed": True, 'msg': 'git remote command failed'})
        sys.exit(1)
    if repo not in data[1]:
        init_data = commands.getstatusoutput("git clone %s ." % repo)
        if init_data[0] != 0:
            print json.dumps({"failed": True, 'msg': 'git clone failed'})
            sys.exit(1)
    commands.getstatusoutput("git clean -f && git pull")
    checkout_data = commands.getstatusoutput("git checkout %s" % tag)
    if checkout_data[0] == 0:
        print json.dumps({'msg': '当前版本：%s' % tag})
        sys.exit()
    else:
        print json.dumps({"failed": True, 'msg': 'tag 错误，请检查'})
else:
    print json.dumps({"failed": True, "msg": "参数不全: dest repo tag"})
    sys.exit(1)
