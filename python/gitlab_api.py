#!/usr/bin/python
# _*_coding:utf-8 _*_
# import sys
import json
import requests

# userid = 83
token = '***********'


class JOB_INFO():

    def __init__(self, *args, **kwargs):
        self.url = 'https://***.com/api/v3/projects?private_token=%s' % token
        r = requests.get(self.url, verify=False)
        self.data = json.loads(r.text)
        # print self.data

    def urls(self):
        i = {}
        for a in self.data:
            i[a['name']] = a['ssh_url_to_repo']
        return i

    def job_id(self):
        i = {}
        for a in self.data:
            i[a['ssh_url_to_repo']] = a['id']
        return i


def create_job(name):
    url = 'https://***.com/api/v3/projects?private_token=%s' % token
    data = {
        'name': name,
        'visibility': 'private'
    }
    r = requests.post(url, json=data, verify=False)
    data = json.loads(r.text)
    return data['ssh_url_to_repo']


def get_commits(id):
    url = 'https://***.com/api/v3/projects/%s/repository/commits?private_token=%s' % (id, token)
    r = requests.get(url, verify=False)
    data = json.loads(r.text)
    return data


if __name__ == '__main__':
    job_info = JOB_INFO()
    name = 'git@***.com:chengongliang/z_test2.git'
    d = job_info.urls()
    ids = job_info.job_id()
    print get_commits(ids[name])
    # if name in d:
    #     print d[name]
    # else:
    #     print create_job(name)
