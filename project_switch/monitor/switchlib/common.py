#!/usr/bin/env python3

import re, decorator

@decorator.rrd_options(DS=('input_rate', 'output_rate'), DST='COUNTER')
def IO_rate(get_oid, interface):
    in_oct = get_oid('1.3.6.1.2.1.2.2.1.10.'+str(interface))
    out_oct = get_oid('1.3.6.1.2.1.2.2.1.16.'+str(interface))
    return (in_oct, out_oct)

def name(self, get_oid):
    r = get_oid('1.3.6.1.2.1.1.5.0')

def get_if_index(self):
    r = [ int(x) for x in re.findall('INTEGER: (.*)\n', self.walk_oid('1.3.6.1.2.1.2.2.1.1')) ]
    return r

def get_if_desc(self):
    r = re.findall('STRING: (.*)\n', self.walk_oid('1.3.6.1.2.1.2.2.1.2'))
    return r

def get_if_stat(self):
    r = re.findall('INTEGER: (.*)\([12]\)\n', self.walk_oid('1.3.6.1.2.1.2.2.1.8'))
    return r

def get_if_inOctets(self):
    r = [ int(x) for x in re.findall('Counter64: (.*)\n', self.walk_oid('1.3.6.1.2.1.31.1.1.1.6')) ]
    return r

def get_if_outOctets(self):
    r = [ int(x) for x in re.findall('Counter64: (.*)\n', self.walk_oid('1.3.6.1.2.1.31.1.1.1.10')) ]
    return r

def get_if_speed(self):
    r = [ int(x) for x in re.findall('Gauge32: (.*)\n', self.walk_oid('1.3.6.1.2.1.31.1.1.1.15')) ]
    return r

def get_if_inMulticastPkts(self):
    r = [ int(x) for x in re.findall('Gauge32: (.*)\n', self.walk_oid('1.3.6.1.2.1.31.1.1.1.8')) ]
    return r

def get_if_outMulticastPkts(self):
    r = [ int(x) for x in re.findall('Gauge32: (.*)\n', self.walk_oid('1.3.6.1.2.1.31.1.1.1.12')) ]
    return r

def get_if_inBroadcastPkts(self):
    r = [ int(x) for x in re.findall('Gauge32: (.*)\n', self.walk_oid('1.3.6.1.2.1.31.1.1.1.9')) ]
    return r

def get_if_outBroadcastPkts(self):
    r = [ int(x) for x in re.findall('Gauge32: (.*)\n', self.walk_oid('1.3.6.1.2.1.31.1.1.1.13')) ]
    return r
