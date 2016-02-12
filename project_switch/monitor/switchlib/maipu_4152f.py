#!/usr/bin/env python3

import re, sys
import decorator

# function "get_oid" and "walk_oid" has been import dynamicly by class.py
@decorator.rrd_options(DS='memory_uility')
def memory(get_oid):
    #total = int(re.search('INTEGER: (.*)\n', get_oid('1.3.6.1.4.1.5651.100.1.8.1.4.1')).group(1))
    #used = int(re.search('INTEGER: (.*)\n', get_oid('1.3.6.1.4.1.5651.100.1.8.1.6.1')).group(1))
    #r = round(used/total*100)
    #return (r,)
    return None

@decorator.rrd_options(DS='CPU_uility')
def cpu(get_oid):
    r = 100 - int(re.search('Last  5 second CPU IDLE:  (.*)%\n', get_oid('1.3.6.1.4.1.5651.100.1.8.1.3.1')).group(1))
    return (r,)
