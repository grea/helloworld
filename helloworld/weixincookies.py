# encoding=utf-8
import json
import requests
import math
import random

myWeixin = [
    {'no': '18518986909', 'psw': '2016@sogou.com'},
    #{'no': 'shudieful3618@163.com', 'psw': 'a123456'},
]

def get_wxltoken():
    def s4():
        s = "%4x" % math.floor((1 + random.random()) * 65536)
        return s[1::]
    token = "%s%s%s%s%s%s%s%s" % (s4(), s4(), s4(), s4(), s4(), s4(), s4(), s4())
    print "=======%s========" % token
    return token

def getCookies(weixin):
    """ 获取Cookies """
    cookies = []
    loginURL = r'https://account.sogou.com/web/login'
    for elem in weixin:
        account = elem['no']
        password = elem['psw']
        #username = base64.b64encode(account.encode('utf-8')).decode('utf-8')
        postData = {
		'username':account,
    		'password':password,
    		'captcha':'',
    		'client_id':'2017',
    		'xd':'http://www.sogou.com/jump.htm',
                'token':get_wxltoken
                
        }
        session = requests.Session()
        r = session.post(loginURL, data=postData)
        cookie = session.cookies.get_dict()
        cookies.append(cookie)
        #jsonStr = r.content.decode('gbk')
        #info = json.loads(jsonStr)
        #if info["retcode"] == "0":
        #    print "Get Cookie Success!( Account:%s )" % account
        #    cookie = session.cookies.get_dict()
        #    cookies.append(cookie)
        #else:
        #    print "Failed!( Reason:%s )" % info['reason']
    return cookies


weixincookies = getCookies(myWeixin)
print "Get Cookies Finish!( Num:%d)" % len(weixincookies)
print "token is %s " % get_wxltoken()
