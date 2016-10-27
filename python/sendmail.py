#!/usr/bin/env python
#coding:utf8

import sys
import smtplib
from email.mime.text import MIMEText

def send_mail(to_list,sub,content):
    mail_host="smtp.***.com" 
    mail_user="chengongliang@****.com"
    mail_pass="123456"
    me="chengongliang@***.com"
    msg = MIMEText(content,_subtype='html',_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = "chengongliang@***.com"
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
if __name__ == '__main__':
    mail_list = sys.argv[1].split(',')
    send_mail(mail_list,sys.argv[2],sys.argv[3])
