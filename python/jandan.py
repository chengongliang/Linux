#!/usr/bin/python
#encoding:utf8
#author:chengongliang

import re
import sys
import requests

def getHtml(url):
    headers1 = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

    request = requests.get(url, headers=headers1)
    if request.ok:
        html = request.content
        return html
    else:
        request = requests.get(url, headers=headers2)
        if request.ok:
            html = request.content
            return html
        else:
            print "连接服务器失败，错误码：%s" % request.status_code
            sys.exit(1)

def getUrl_list(html):
    re_img = re.compile(r'<div class="text">.*?<p>.*?<a href="(http://ww.*?)".*?<div class="vote".*?<span id="cos_support.*?">(\d+)</span>.*?<span id="cos_unsupport.*?">(\d+)</span>', re.S)
    url_list = []
    items = re_img.findall(html)
    for url,oo,xx in items:
        if int(oo) >= 200 and int(xx) <= 30:
            url_list.append(url)
    return url_list

def getCurrent():
    start_page = getHtml("http://jandan.net/ooxx")
    current = re.compile(r'<div class="comments">.*?<span class="current-comment-page">\[(\d+)\]</span>',re.S)
    page = current.findall(start_page)[0]
    return page

def save_img(url,name):
    with open(name, 'wb') as fd:
        img = getHtml(url)
        fd.write(img)

def download(url_list):
    for url in url_list:
        name = url.split('/')[-1]
        save_img(url,name)

def main():
    page = getCurrent()
    list_pages = range(int(page)-10,int(page)+1)
    print list_pages
    for p in list_pages:
        url = 'http://jandan.net/ooxx/page-%s#comments' % p
        print "~~正在下载第%s页~~" % p
        html = getHtml(url)
        url_list = getUrl_list(html)
        download(url_list)

if __name__ == "__main__":
    main()
