#!/usr/bin/python
#encoding:utf8
#author:chengongliang

import re
import os
import sys
#import random
import requests
from sql import mySQL
from conf import setting

s = mySQL()
def getHtml(url):
    n = 0
    #agent = setting.configs['agents']
    agent = s.get_agent()
    while n < len(agent):
        headers = {'User-Agent':agent[n]}
        request = requests.get(url, headers=headers)
        if request.ok:
            html = request.content
            return html
            break
        else:
            n += 1
    print "连接服务器失败，错误码：%s" % request.status_code
    sys.exit(1)


def getUrl_list(html):
    re_img = re.compile(r'<div class="text">.*?<p>.*?<a href="(http://ww.*?)".*?<div class="vote".*?<span id="cos_support.*?">(\d+)</span>.*?<span id="cos_unsupport.*?">(\d+)</span>', re.S)
    url_list = []
    items = re_img.findall(html)
    for url,oo,xx in items:
        if int(oo) >= 150 and int(xx) <= 30:
            s.put_ooxx(url,oo,xx)
            url_list.append(url)
    return url_list

def getCurrent():
    start_page = getHtml("http://jandan.net/ooxx")
    current = re.compile(r'<div class="comments">.*?<span class="current-comment-page">\[(\d+)\]</span>',re.S)
    page = current.findall(start_page)[0]
    #s = mySQL()
    s.put_num('page_num',page)
    #with open('page_num','w') as fd:
    #    fd.write(str(page))
    return page

#def getLast():
#    if os.path.exists('conf/page_num'):
#        with open('conf/page_num','r') as fd:
#            return fd.read()
#    else:
#        return getCurrent()

def save_img(url,name):
    if not os.path.exists('src/%s' %name):
        with open('src/%s' %name, 'wb') as fd:
            img = getHtml(url)
            fd.write(img)

def download(url_list):
    for url in url_list:
        name = url.split('/')[-1]
        save_img(url,name)

def main():
    last_num = s.get_num()
    current_num = getCurrent()
    list_pages = range(int(last_num),int(current_num)+1)
    print list_pages
    for p in list_pages:
        url = 'http://jandan.net/ooxx/page-%s#comments' % p
        print "~~正在下载第%s页~~" % p
        html = getHtml(url)
        url_list = getUrl_list(html)
        download(url_list)
    s.close()
