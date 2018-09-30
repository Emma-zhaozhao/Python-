#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests
from urllib.parse import urlencode
import re
import csv
import time

# 获取网页数据
def get_page(num):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
    params = {
        'start': str(num),
        'limit': '20',
        'sort': 'new_score',
        'status': 'P'
    }
    url = 'https://movie.douban.com/subject/1295644/comments?' + urlencode(params)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
    except EOFError as e:
        print(e)
        return None


# 解析网页代码
def parse_page(html):
    info = []
    pattern = re.compile(r'<div class="comment">.*?<a href=.*?class="">'
                         r'(.*?)</a>.*?<span class=.*?title="(.*?)"></span>.*?'
                         r'<span class="comment-time " title="(.*?)">.*?</span>.*?'
                         r'<span class="short">(.*?)</span>.*?</div>', re.S)
    items = re.findall(pattern, html)

    for item in items:
        comic = {}
        comic['UserName'] = item[0].strip()
        comic['Star'] = item[1].strip()
        comic['Time'] = item[2].strip()
        comic['Comment'] = item[3].strip().split()
        info.append(comic)
    return info


# 保存数据
def write_to_file(info):
    with open('《这个杀手不太冷》影评4.csv', 'a', newline='') as csvfile:
        fieldnames = ['UserName', 'Star', 'Time', 'Comment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        try:
            writer.writerows(info)
        except:
            pass


# 执行函数
def main():
    for i in range(10):
        num = i * 20
        html = get_page(num)
        info = parse_page(html)
        write_to_file(info)
        print('本页采集完毕')
        time.sleep(1)


if __name__ == '__main__':
    main()





