#!/usr/bin/env python3

import re, decorator

@decorator.rrd_options(DS=('input_rate', 'output_rate'), DST='COUNTER')
def IO_rate(get_oid, interface):
    in_oct = get_oid('1.3.6.1.2.1.2.2.1.10.'+str(interface))
    out_oct = get_oid('1.3.6.1.2.1.2.2.1.16.'+str(interface))
    return (in_oct, out_oct)

def name(get_oid):
    r = get_oid('1.3.6.1.2.1.1.5.0')
    return (r,)
