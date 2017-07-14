#!/usr/bin/python
# _*_coding:utf-8 _*_
import sys
import json
import requests


class WE():

    def __init__(self):
        self.corpid = 'corpid'
        self.corpsecret = 'corpsecret'
        self.accesstoken = self.gettoken()
        self.user = 'all'

    def gettoken(self):
        gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + \
            self.corpid + '&corpsecret=' + self.corpsecret
        try:
            token_file = requests.get(gettoken_url)
        except Exception, e:
            print e
            sys.exit()
        token_data = token_file.text
        token_json = json.loads(token_data)
        token = token_json['access_token']
        # print token
        return token

    def senddata(self, content):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.accesstoken
        send_values = {
            "touser": self.user,  # 企业号中的用户帐号，在zabbix用户Media中配置，如果配置不正常，将按部门发送。
            # "touser": "chengongliang",  # 企业号中的用户帐号，在zabbix用户Media中配置，如果配置不正常，将按部门发送。
            "toparty": "1",  # 企业号中的部门id。
            "msgtype": "text",  # 消息类型。
            "agentid": "1000003",  # 企业号中的应用id。
            "text": {
                "content": content
            },
            "safe": "0"
        }
        r = requests.post(send_url, json=send_values)
        print r.text


# we = WE()
# we.senddata('sss')
