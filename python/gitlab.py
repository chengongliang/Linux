#!/usr/bin/python
#_*_ coding:utf-8 _*_
import os
import sys
import json
import requests
from optparse import OptionParser


class GitApi():

    def __init__(self, *args, **kwargs):
        self.base_url = 'http://test.aaa.com/api/v3/'
        self.token = 'okLuMsU7y1dPukxHDzrq' # deploy

    def _get(self, url):
        r = requests.get(url, verify=False)
        data = json.loads(r.text)
        return data

    def _post(self, url, payloads):
        p = requests.post(url, params=payloads, verify=False)
        data = json.loads(p.text)
        return data

    def _put(self, url, payloads):
        p = requests.put(url, headers=payloads, verify=False)
        if p.status_code == 200:
            data = json.loads(p.text)
            return data
        else:
            return "Error: %s" % p.status_code

    def _delete(self, url):
        p = requests.delete(url, verify=False)
        data = json.loads(p.text)
        return data

    def get_id_url(self, project_name):
        url = self.base_url + 'projects/all?page=1&per_page=100&private_token=%s&search=%s' % (self.token, project_name)
        data = self._get(url)
        try:
            repo_id, repo_url = self.job_idArepo_url(data, project_name)
        except Exception, e:
            print 'project not exist.'
            sys.exit()
        return repo_id, repo_url

    def job_idArepo_url(self, data, project_name):
        repos, ids = {}, {}
        for i in data:
            repos[i['name']] = i['ssh_url_to_repo']
            ids[i['name']] = i['id']
        return ids[project_name], repos[project_name]

    def protected_branch(self, project_name, branch, action="protect"):
        pro_id, _ = self.get_id_url(project_name)
        if action == "protect":
            url = self.base_url + 'projects/%s/repository/branches/%s/protect' % (pro_id, branch)
        else:
            url = self.base_url + 'projects/%s/repository/branches/%s/unprotect' % (pro_id, branch)

        payloads = {'PRIVATE-TOKEN': self.token}
        data = self._put(url, payloads)
        return data

    def create_job(self, project_name, space):
        url = self.base_url + 'projects?private_token=%s' % self.token
        space_id = self.get_groups()[space]
        payloads = {'name': project_name, 'visibility': 'private', 'namespace_id': space_id}
        data = self._post(url, payloads)
        try:
            return data['id'], data['ssh_url_to_repo'], data['http_url_to_repo']
        except KeyError:
            return 'project already exist.', self.get_id_url(project_name)

    def get_commits(self, repo_id):
        url = self.base_url + 'projects/%s/repository/commits?private_token=%s' % (
            repo_id, self.token)
        data = self.__get(url)
        return data

    def get_single_commit(self, id, sha):
        url = self.base_url + 'projects/%s/repository/commits/%s/diff?private_token=%s' % (
            id, sha, self.token)
        data = self._get(url)
        return data

    def get_user_id(self, username):
        url = self.base_url + 'users?search=%s&private_token=%s' % (username, self.token)
        data = self._get(url)
        try:
            user_id = data[0]['id']
        except Exception, e:
            print "user not exist."
            sys.exit()
        return user_id

    def get_groups(self):
        url = self.base_url + 'groups?private_token=%s' % self.token
        data = self._get(url)
        # groups = {g['name']: g['id'] for g in data}
        groups = {}
        for g in data:
            groups[g['name']] = g['id']
        return groups

    def add_mem(self, **kwargs):
        if 'gid' in kwargs:
            url = self.base_url + 'groups/%s/members/?private_token=%s' % (kwargs['gid'], self.token)
        elif 'pid' in kwargs:
            url = self.base_url + 'projects/%s/members/?private_token=%s' % (kwargs['pid'], self.token)
        payloads = {'user_id': kwargs['uid'], 'access_level': kwargs['access_level']}
        data = self._post(url, payloads)
        return data

    def del_mem(self, **kwargs):
        if 'gid' in kwargs:
            url = self.base_url + 'groups/%s/members/%s?private_token=%s' % (kwargs['gid'], kwargs['uid'], self.token)
        elif 'pid' in kwargs:
            url = self.base_url + 'projects/%s/members/%s?private_token=%s' % (kwargs['pid'], kwargs['uid'], self.token)
        data = self._delete(url)
        return data


def main():
    parser = OptionParser()
    parser.add_option('-m','--method',
                      dest='method',
                      action='store',
                      help='create, addmem, delmem, protect, unprotect')
    parser.add_option('-g','--group',
                      dest='group',
                      action='store',
                      help='group name')
    parser.add_option('-u','--username',
                      dest='username',
                      action='store',
                      help='username')
    parser.add_option('-p','--project',
                      dest='projectname',
                      action='store',
                      help='projectname')
    parser.add_option('-b','--branch',
                      dest='branch',
                      action='store',
                      default='master',
                      help='branch')
    parser.add_option('-l','--level',
                      dest='level',
                      action='store',
                      default=30,
                      help='access_level')
    options, args = parser.parse_args()
    # groups = {u'pp': 47, u'php': 215, u'datasearch': 14, u'spider': 23, u'spider_new': 150,
    #           u'pubilc': 222, u'front': 53, u'miojiall': 69, u'op': 19}
    level = options.level
    method = options.method
    group_name = options.group
    user_name = options.username
    project_name = options.projectname
    branch = options.branch

    gapi = GitApi()
    if not method or len(method) < 2:
        os.system('%s -h' % __file__)
    elif method in 'create':
        print gapi.create_job(project_name, group_name)
    elif method in 'protect':
        print gapi.protected_branch(project_name, branch)
    elif method == 'unprotect':
        print gapi.protected_branch(project_name, branch, 'unprotected')
    elif method in 'addmem':
        user_id = gapi.get_user_id(user_name)
        if group_name or project_name:
            try:
                groups = gapi.get_groups()
                print gapi.add_mem(gid=groups[group_name], uid=user_id, access_level=level)
            except KeyError, e:
                project_id, _ = gapi.get_id_url(project_name)
                print gapi.add_mem(pid=project_id, uid=user_id, access_level=level)
                # print project_id
            except Exception, e:
                print "Error: group --> %s not exist." % e
        else:
            os.system('%s -h' % __file__)
    elif method in 'delmem':
        user_id = gapi.get_user_id(user_name)
        if group_name or project_name:
            try:
                groups = gapi.get_groups()
                print gapi.del_mem(gid=groups[group_name], uid=user_id)
            except KeyError, e:
                project_id, _ = gapi.get_id_url(project_name)
                print gapi.del_mem(pid=project_id, uid=user_id)
                # print project_id
            except Exception, e:
                print "Error: group --> %s not exist." % e
        else:
            os.system('%s -h' % __file__)
    else:
        print 'wrong method'
        sys.exit()


if __name__ == '__main__':
    main()
