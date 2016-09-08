#!/usr/bin/python
#encoding:utf8

import re
import sys
import random
import cookielib
import urllib, urllib2

def getHtml(url):
 #   headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    #proxies = ['180.103.131.65:808','124.240.187.78:81','118.180.15.152:8102']
    #proxy = random.choice(proxies)
    #proxy_support = urllib2.ProxyHandler({'http':proxy})
    #opener = urllib2.build_opener(proxy_support)
    #urllib2.install_opener(opener)

    try:
        request = urllib2.Request(url, headers=headers)
        response = opener.open(request)
        html = response.read()
        return html
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print "连接服务器失败,错误代码: %s" %e.code
            return None
        if hasattr(e, "reason"):
            print "连接服务器失败,错误原因: %s" %e.reason
            return None

def getUrl_list(html):
    re_img = re.compile(r'<div class="text">.*?<p>.*?<img src="(http://ww.*?)".*?<div class="vote".*?<span id="cos_support.*?">(\d+)</span>.*?<span id="cos_unsupport.*?">(\d+)</span>', re.S)
    url_list = []
    items = re_img.findall(html)
    for url,oo,xx in items:
        if int(oo) >= 200 and int(xx) <= 30:
            url_list.append(url)
            if url[-3:] == 'gif':
                index = url_list.index(url)
                re_gif = re.compile(r'%s.*?org_src="(.*?)"'%url)
                org_url = re_gif.findall(html)
                url_list[index] = org_url[0]
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

def download(html, url_list):
    url_list = getUrl_list(html)
    for url in url_list:
        name = url.split('/')[-1]
        save_img(url,name)

def main():
    page = getCurrent()
    list_pages = range(int(page)-10,int(page)+1)
    print list_pages
    for p in list_pages:
        url = 'http://jandan.net/ooxx/page-%s#comments' % p
        html = getHtml(url)
        url_list = getUrl_list(html)
        download(html,url_list)

if __name__ == "__main__":
    main()
