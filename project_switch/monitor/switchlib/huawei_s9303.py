#!/usr/bin/env python3

import re, sys
import decorator

# function "get_oid" and "walk_oid" has been import dynamicly by class.py
@decorator.rrd_options(DS=('memory_1_uility', 'memory_2_uility'))
def memory(get_oid):
    r1 = get_oid('1.3.6.1.4.1.2011.5.25.31.1.1.1.1.7.11')
    r2 = get_oid('1.3.6.1.4.1.2011.5.25.31.1.1.1.1.7.12')
    return (r1, r2)

@decorator.rrd_options(DS=('CPU_1_uility', 'CPU_2_uility'))
def cpu(get_oid):
    r1 = get_oid('1.3.6.1.4.1.2011.5.25.31.1.1.1.1.5.11')
    r2 = get_oid('1.3.6.1.4.1.2011.5.25.31.1.1.1.1.5.12')
    return (r1, r2)
