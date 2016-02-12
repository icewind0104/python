#!/bin/usr/env python3
# -*- coding: utf-8 -*-

class configs():
    web_path = '/home/meidl/python'
    root_path = '/home/meidl/python/project_switch/monitor'
    RRD_save_path = root_path + '/rra_test'    # !
    graph_save_path = '/static'

    db = {
        'host' : '192.168.150.131',
        'port' : 3306,
        'user' : 'root',
        'password' : 'my&sql',
        'db' : 'test_moni',    # !
        'maxsize' : 10,
        'minsize' : 1
    }

    server = {
        'host' : '192.168.150.140',
        'port' : 8000
    }

    log = {
        'path' : root_path + '/log'
    }

# advance

    rrd_create_option_default = {
        'DS' : 'DS',
        'DST' : 'GAUGE',
        'step' : '300',
        'max' : 'U',
        'min' : '0',
        'CF' : 'AVERAGE',
        'CDP' : '1',
        'size' : '600'        
    }

    common_indicator = {
        'cpu' : None,
        'memory' : None
    }

    graph_default_color = ['#00AA00', '#AA0000', '#0000AA']
