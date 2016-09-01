#!/usr/bin/python
#encoding:utf8

import re
import sys
import urllib, urllib2

def getHtml(url):
   # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
   # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/42.0'}
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        html = response.read()
        return html
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print "连接服务器失败,错误代码: %s" %e.code
            return None
        if hasattr(e, "reason"):
            print "连接服务器失败,错误原因: %s" %e.reason
            return None

def getUrl(html):
    re_img = re.compile(r'<div class="text">.*?<p>.*?<img src="(http://ww.*?)".*?<div class="vote".*?<span id="cos_support.*?">(\d+)</span>.*?<span id="cos_unsupport.*?">(\d+)</span>', re.S)
    items = re_img.findall(html)
    url_list = []
    for url,oo,xx in items:
        if int(oo)/int(xx) > 5:
            url_list.append(url)
    return url_list

def getCurrent():
    start_page = getHtml("http://jandan.net/ooxx")
    current = re.compile(r'<div class="comments">.*?<span class="current-comment-page">\[(\d+)\]</span>',re.S)
    page = current.findall(start_page)[0]
    return page

def download(url_list):
    i = 1
    for url in url_list:
        if url[-3:] == "jpg":
            try:
                urllib.urlretrieve(url, filename="%s.jpg" %i)
                i += 1
            except urllib.ContentTooShortError:
                print "Network conditions is not good.Reloading"
                urllib.urlretrieve(url, filename="%s.jpg" %i)
        elif url[-3:] == "gif":
            re_gif = re.compile(r'%s.*?org_src="(.*?)"'%url)
            org_url = re_gif.findall(html)
            urllib.urlretrieve(org_url[0], filename="%s.gif" %i)
            i += 1

if __name__ == "__main__":
    page = getCurrent()
    url = 'http://jandan.net/ooxx/page-%s#comments' % page
    html = getHtml(url)
    url_list = getUrl(html)
    print url_list
    #download(url_list)
