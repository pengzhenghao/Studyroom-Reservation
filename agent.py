import re

import cv2
import requests


class Agent(object):
    def __init__(self, username=None, password=None):
        if not username or not password:
            username = input('请输入账户:')
            password = input('请输入密码:')

        self.username = username
        self.password = password
        self.sess = requests.session()
        self.sess.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        }
        self.login()

    def login(self):
        r = self.sess.get('http://studyroom.lib.sjtu.edu.cn/')
        captcha_url = 'https://jaccount.sjtu.edu.cn/jaccount/' + re.search(r'<img src="(captcha\?\d*?)"',
                                                                           r.content.decode()).group(1)
        captcha = self.sess.get(captcha_url)
        with open('captcha.png', 'wb') as file:
            file.write(captcha.content)
        cv2.imshow(u'验证码', cv2.imread('captcha.png'))
        captcha = input("请输入验证码")

        qs = re.search(r'sid=(.*?)&returl=(.*?)&se=(.*)', r.url)

        data = {
            'sid': qs.group(1),
            'returl': qs.group(2),
            'se': qs.group(3),
            'v': "",
            'user': self.username,
            'pass': self.password,
            'captcha': captcha}
        result = self.sess.post('https://jaccount.sjtu.edu.cn/jaccount/ulogin?' + qs.group(0), data=data, )

        if re.search(u'图书馆空间场馆预约系统', result.content.decode()):
            print('登录成功')
        elif re.search(u'请正确填写你的用户名和密码', result.content.decode()):
            print('请正确填写你的用户名和密码')
        elif re.search(u'请正确填写验证码', result.content.decode()):
            print('请正确填写验证码')
        else:
            print('登录失败')

    def join(self, room=None, pw=None):
        if not room or not pw:
            room = input('请输入房号:')
            pw = input('请输入密码:')
        url = 'http://studyroom.lib.sjtu.edu.cn/reserve_plus.asp?applicationid=' + str(room)
        response = self.sess.get(url=url)
        pat = r"<input type='hidden' value='(\d)' name='needusernum'/><input type='hidden' value='(.*?)' name='roomname'"
        regular = re.search(pat, response.content.decode())

        if regular:
            print(u'找到此房间, 即将进行申请')
            url = 'http://studyroom.lib.sjtu.edu.cn/reserve_plus_ok.asp'
            data = {'password': pw, 'B1': u'加入', 'applicationid': room, 'needusernum': regular.group(1),
                    'roomname': regular.group(2)}
            response = self.sess.post(url, data)
            s = re.search(r"language=javascript>alert\('(.*?)'\);", response.content.decode())
            if s:
                print(s.group(1))
                return
            else:
                print('爆炸了')
                return
        else:
            print('登录失败')

    def join(self, room=None, pw=None):
        if not room or not pw:
            room = input('请输入房号:')
            pw = input('请输入密码:')

        url = 'http://studyroom.lib.sjtu.edu.cn/reserve_plus.asp?applicationid=' + str(room)
        response = self.sess.get(url=url)

        pat = r"<input type='hidden' value='(\d)' name='needusernum'/><input type='hidden' value='(.*?)' name='roomname'"
        regular = re.search(pat, response.content.decode())

        if regular:
            print(u'找到此房间, 即将进行申请')
            url = 'http://studyroom.lib.sjtu.edu.cn/reserve_plus_ok.asp'
            data = {'password': pw, 'B1': u'加入', 'applicationid': room, 'needusernum': regular.group(1),
                    'roomname': regular.group(2)}
            response = self.sess.post(url, data)
            s = re.search(r"language=javascript>alert\('(.*?)'\);", response.content.decode())
            if s:
                print(s.group(1))
                return
            else:
                print('爆炸了')
                return
        else:
            print(u'未找到此房间, 退出申请')
            print(response.content.decode())
            return


if __name__ == '__main__':
    print('请从main.py进入程序')
    pass
