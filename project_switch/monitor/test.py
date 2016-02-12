#!/usr/bin/python3

import sys, time
sys.path.append('/home/meidl/python')
import asyncio
from orm import *
from models import *
import rrd_tools, switch_tools
import inspect
import db

#rrd_tools.create(config.configs.RRD_save_path+'1.rrd', step=60, DSnum=3)
#update(config.configs.RRD_save_path+'1.rrd', 10)
#lookup(config.configs.RRD_save_path+'1.rrd')
#print(tools.get_max(config.configs.RRD_save_path+'1.rrd'))
#rrd_tools.get_last_value(config.configs.RRD_save_path+'1.rrd')

'''
def init(loop):
    pool = yield from create_pool(host='192.168.150.131', password='my&sql', user='root', db='monitor', loop=loop)
    rs = yield from switches.findall()
    for each in rs:
        switch = switches(**each)
        switch.create_rrd()
    exit()

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
'''

A = switch_tools.device(id=1, host='1.1.1.1', vendor='maipu', model='4152f')
A.create_rrd('memory')
