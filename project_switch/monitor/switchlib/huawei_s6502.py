#!/usr/bin/env python3

import re, sys
import decorator

# function "get_oid" and "walk_oid" has been import dynamicly by class.py
@decorator.rrd_options(DS=('memory_1_uility', 'memory_2_uility'))
def memory(get_oid):
    total = get_oid('1.3.6.1.4.1.2011.6.1.2.1.1.2.0')
    free = get_oid('1.3.6.1.4.1.2011.6.1.2.1.1.3.0')
    r1 = round((total-free)/total*100)
    total = get_oid('1.3.6.1.4.1.2011.6.1.2.1.1.2.1')
    free = get_oid('1.3.6.1.4.1.2011.6.1.2.1.1.3.1')
    r2 = round((total-free)/total*100)
    return (r1, r2)

@decorator.rrd_options(DS=('CPU_1_uility', 'CPU_2_uility'))
def cpu(get_oid):
    r1 = get_oid('1.3.6.1.4.1.2011.6.1.1.1.2.0')
    r2 = get_oid('1.3.6.1.4.1.2011.6.1.1.1.2.1')
    return (r1, r2)
