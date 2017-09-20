import re

from agent import Agent

if __name__ == '__main__':
    a1 = Agent('jaccount', 'password')
    a2 = Agent('jaccount', 'password')

    data = input('请复制表格')

    pat = re.compile(r'(\d{6}).*?(\d{6})')
    data = re.findall(pat, data)

    for k, v in data:
        print('现在申请的房号是:%d', k)
        a1.join(k, v)
        a2.join(k, v)
