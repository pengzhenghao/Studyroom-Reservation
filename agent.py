import re
import cv2
import requests


class Agent(object):
    def __init__(self, username=None, passsword=None):
        if not username or not passsword:
            print('请输入账户密码')
            input(username, passsword)

        self.username = username
        self.password = passsword
        self.sess = requests.session()
        self.login()

    def login(self):
        url = 'http://studyroom.lib.sjtu.edu.cn/'
        headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        }
        r = self.sess.get(url,headers=headers)

        captcha_url = 'https://jaccount.sjtu.edu.cn/jaccount/' + re.search(r'<img src="(captcha\?\d*?)"', r.content.decode()).group(1)
        captcha = self.sess.get(captcha_url)
        with open('captcha.png', 'wb') as file:
            file.write(captcha.content)
        cv2.imshow(u'验证码', cv2.imread('captcha.png'))
        captcha = input("请输入验证码")

        login_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://jaccount.sjtu.edu.cn',
            'referer': r.url,
            'Host':'jaccount.sjtu.edu.cn',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        }
        qs = re.search(r'sid=(.*?)&returl=(.*?)&se=(.*)', r.url)

        data = {
            'sid': qs.group(1),
            'returl': qs.group(2),
            'se': qs.group(3),
            'v': "",
            'user': self.username,
            'pass': self.password,
            'captcha': captcha
        }
        result = self.sess.post('https://jaccount.sjtu.edu.cn/jaccount/ulogin?'+qs.group(0), headers=headers, data=data,)

        if re.search(u'图书馆空间场馆预约系统',result.content.decode()):
            print('登录成功')
        else:
            print(result.content.decode())

if __name__=='__main__':
    pass
