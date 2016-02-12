#!/usr/bin/env python3

import re, sys
import decorator

# function "get_oid" and "walk_oid" has been import dynamicly by class.py
@decorator.rrd_options(DS='memory_uility')
def memory(get_oid):
    total = get_oid('1.3.6.1.4.1.2011.6.1.2.1.1.2.65536')
    free = get_oid('1.3.6.1.4.1.2011.6.1.2.1.1.3.65536')
    r = round((total-free)/total*100)
    return (r,)

@decorator.rrd_options(DS='CPU_uility')
def cpu(get_oid):
    r = get_oid('1.3.6.1.4.1.2011.6.1.1.1.2.65536')
    return (r,)
