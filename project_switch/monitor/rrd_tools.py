#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, os
import config
default = config.configs.rrd_create_option_default

def create(fname, DS, **kw):
    cmd = 'rrdtool create %s --step %s ' % (fname, kw.get('step', default['step']))
    for i in DS:
        cmd += 'DS:%s:%s:%s:%s:%s ' % (i, kw.get('DST', default['DST']), str(int(kw.get('step', default['step']))*2), kw.get('min', default['min']), kw.get('max', default['max']))
    cmd += 'RRA:%s:0.5:%s:%s' % (kw.get('CF', default['CF']), kw.get('CDP', default['CDP']), kw.get('size', default['size']))
    #print(cmd)
    os.system(cmd)

def update(fname, value, time=time.time()):
    cmd = 'rrdtool update %s %s' % (fname, time)
    if not isinstance(value, list) and not isinstance(value, tuple):
        value = (value,)
    for i in value:
        cmd += ':%s' % (str(i))
    #print(cmd)
    os.system(cmd)

def lookup(fname, CF='AVERAGE'):
    cmd = 'rrdtool fetch %s %s' % (fname, CF)
    r = ''.join(list(os.popen(cmd)))
    print(r)

def get_last_update(fname):
    cmd = 'rrdtool lastupdate %s' % (fname)
    rstr = list(os.popen(cmd))[2]
    r = rstr.split()
    r[0] = r[0][:-1]
    return tuple(r)

def get_last_value(fname, CF=default['CF']):
    cmd = 'rrdtool info %s' % (fname)
    op = os.popen(cmd)
    rstr = op.readlines()[2]
    step = (rstr[:-1].split())[2]
    cmd = 'rrdtool fetch %s %s --start %s --end %s' % (fname, CF, int(time.time())-int(step), int(time.time()))
    op = os.popen(cmd)
    rstr = op.readlines()[2]
    r = rstr[:-1].split()
    return r[1:]

def get_max(fname, CF=default['CF']):
    cmd = 'rrdtool fetch %s %s' % (fname, CF)
    rlist = list(os.popen(cmd))[2:]
    DSnum = len(rlist[0][:-1].split()) - 1
    L = [None] * DSnum
    for index in range(len(L)):
        L[index] = []
    for each in rlist:
        for index, value in enumerate((each[:-1].split())[1:]):
            if value != '-nan':
                L[index].append(value)
    r = []
    for i in range(DSnum):
        the_max = max(L[i]) if L[i] else None
        r.append(the_max)
    return r

def get_min(fname, CF='AVERAGE'):
    cmd = 'rrdtool fetch %s %s' % (fname, CF)
    rlist = list(os.popen(cmd))[2:]
    DSnum = len(rlist[0][:-1].split()) - 1
    L = [None] * (DSnum + 1)
    for index in range(len(L)):
        L[index] = []
    for each in rlist:
        for index, value in enumerate(each[:-1].split()):
            if value != '-nan':
                L[index].append(value)
    r = []
    for i in range(1, DSnum+1):
        r.append(min(L[i]))
    return r

def graph(fname, DS, **kw):
    file_name = os.path.basename(fname).replace('.rrd', '.png')
    gname = os.path.join(config.configs.web_path + config.configs.graph_save_path, file_name)
    cmd = 'rrdtool graph %s ' % (gname)
    # 设置时间区间
    cmd += '--start now-1h '
    # 绘制标题
    cmd += '-t "%s" ' % (kw.get('title', os.path.basename(fname)))
    # 绘制Y轴上限下限
    min = kw.get('min', default['min'])
    cmd += '--lower-limit %s ' % min if min != 'U' else ''
    max = kw.get('max', default['max'])
    cmd += '--upper-limit %s ' % max if max != 'U' else ''
    if min != 'U' and max != 'U':
        cmd += '--rigid '
    # 生成图片
    for index, value in enumerate(DS):
        cmd += 'DEF:value%s=%s:%s:%s ' % (index, fname, value, kw.get('CF', default['CF']))
    for index, value in enumerate(DS):
        color = index%(len(config.configs.graph_default_color))
        cmd += 'LINE2:value%s%s:%s ' % (index, config.configs.graph_default_color[color], value)
    cmd += '> /dev/null'
    os.system(cmd)
    return os.path.join(config.configs.graph_save_path, file_name)
    






