#!/usr/bin/python3

from urllib import request
import re
import os
import sys

def download(url, img_name, page_index):
    print('save image %s' % img_name)
    with request.urlopen(url) as f:
        date = f.read()

    save_dir = '/home/meidl/Pictures/%s' % page_index
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    with open('%s/%s' % (save_dir, img_name), 'w+b') as f:
        f.write(date)

def get_img(sub_page):
    with request.urlopen(sub_page) as f:
        date = f.read().decode('gbk')
        img_link = re.findall('zoomfile="(.*?)"', date)
    return img_link

cmd, start_page, end_page = sys.argv
host = 'http://bbs.dabin69.com/'
for i in range(int(start_page),int(end_page)):
    print('start search page %s ...' % i)
    with request.urlopen(host + 'forum-7-%s.html' % i) as f:
        date = f.read().decode('gbk')

    sub_page = re.findall('href="(http://bbs.dabin69.com/thread.*?)"', date)
    sub_page = list(set(sub_page))

    # 获取图片的保存地址
    for each_page in sub_page:
        for each_img in get_img(each_page):
            img_url = host + each_img
            img_name = os.path.basename(each_img)
            download(img_url, img_name, i)


