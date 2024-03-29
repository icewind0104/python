#!/usr/bin/env python3

import re, sys
import decorator

# function "get_oid" and "walk_oid" has been import dynamicly by class.py
@decorator.rrd_options(DS='memory_uility', max=100)
def memory(get_oid):
    used = get_oid('1.3.6.1.4.1.9.9.48.1.1.1.5.1')
    free = get_oid('1.3.6.1.4.1.9.9.48.1.1.1.6.1')
    r = round(used/(used+free)*100)
    return (r,)

@decorator.rrd_options(DS='CPU_uility', max=100)
def cpu(get_oid):
    r = get_oid('1.3.6.1.4.1.9.2.1.56.0')
    return (r,)
