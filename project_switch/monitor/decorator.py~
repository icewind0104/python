#!/usr/bin/env python3

import sys
import config
import collections
import functools

default = config.configs.rrd_create_option_default

def rrd_options(
                   DS		= default['DS'],
                   step		= default['step'],
                   DST		= default['DST'],
                   max		= default['max'],
                   min		= default['min'],
                   CF		= default['CF'],
                   CDP		= default['CDP'],
                   size		= default['size']
               ):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.DS = DS if (isinstance(DS, list) or isinstance(DS, tuple)) else (DS,)
        wrapper.step = step
        wrapper.DST = DST
        wrapper.max = str(max)
        wrapper.min = str(min)
        wrapper.CF = CF
        wrapper.CDP = str(CDP)
        wrapper.size = str(size)
        return wrapper
    return decorator
