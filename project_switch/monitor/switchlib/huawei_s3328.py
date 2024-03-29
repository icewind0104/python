#!/usr/bin/env python3

import re, sys
import decorator

# function "get_oid" and "walk_oid" has been import dynamicly by class.py
@decorator.rrd_options(DS='memory_uility')
def memory(get_oid):
    r = get_oid('1.3.6.1.4.1.2011.5.25.31.1.1.1.1.7.67108873')
    return (r,)

@decorator.rrd_options(DS='CPU_uility')
def cpu(get_oid):
    r = get_oid('1.3.6.1.4.1.2011.5.25.31.1.1.1.1.5.67108873')
    return (r,)
