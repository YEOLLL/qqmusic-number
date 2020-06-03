import requests
import qqmusic_cookie
import json

qqnumber = input('输入QQ号: ')
password = input('输入密码: ')
userurl = input('输入对方主页地址: ')
cookie = qqmusic_cookie.login_for_cookies(qqnumber, password)

userid = userurl.split('=')[1]

params = (
    ('g_tk_new_20200303', '708052'),
    ('g_tk', '708052'),
    #('loginUin', '2761713235'),
    ('hostUin', '0'),
    ('format', 'json'),
    ('inCharset', 'utf8'),
    ('outCharset', 'utf-8'),
    ('notice', '0'),
    ('platform', 'yqq.json'),
    ('needNewCode', '0'),
    ('cid', '205360838'),
    ('ct', '20'),
    ('userid', userid),
    ('reqfrom', '1'),
    ('reqtype', '0'),
)

response = requests.get('https://c.y.qq.com/rsc/fcgi-bin/fcg_get_profile_homepage.fcg', cookies=cookie, params=params)

if (json := response.json())["code"] == 0:
    uin = json["data"]['creator']["uin"]
    print('对方QQ号为: '+str(uin))