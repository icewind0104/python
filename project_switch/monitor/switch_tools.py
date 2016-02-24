#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re, inspect
import rrd_tools
import config
default = config.configs.rrd_create_option_default
import loggings

class device():
    def __init__(self, id, host, vendor, model, snmp_version='2c', snmp_community='public', **kw):
        self._id = str(id)
        self._version = snmp_version
        self._community = snmp_community
        self._host = host
        self._base_snmpget_cmd = ('snmpget -v %s -c %s %s ' % (self._version, self._community, self._host))
        self._base_snmpwalk_cmd = ('snmpwalk -v %s -c %s %s ' % (self._version, self._community, self._host))
        self._model = vendor+'_'+model
        self._mod = __import__('switchlib.'+self._model, globals(), locals(), self._model)
        self._common_mod = __import__('switchlib.common', globals(), locals(), 'common')
        self._dir = config.configs.RRD_save_path+'/switch_id_'+str(id)
        self.loggings = loggings.loggings(config.configs.log['path'], flag=self._host)

        def exec_snmpget(oid):
            output = ''.join(os.popen(self._base_snmpget_cmd+oid))
            if not output:
                raise RuntimeError ('Timeout: No Response from %s' % (self._host))
            date_type, value = re.search('(Gauge32|STRING|INTEGER|Counter32|Counter64): (.*)\n$', output, re.S).group(1,2)
            if date_type != 'STRING':
                value = int(value)
            return value
        self.get_oid = exec_snmpget
        #self._mod.get_oid = self.get_oid    # import function : get_oid into imported model

        def exec_snmpwalk(oid):
            output = ''.join(os.popen(self._base_snmpwalk_cmd+oid))
            if not output:
                raise RuntimeError ('Timeout: No Response from %s' % (self._host))
            #print(output)
            return output
        self.walk_oid = exec_snmpwalk
        #self._mod.walk_oid = self.walk_oid    # import function : walk_oid into imported model

    @property
    def id(self):
        return self._id

    def create_switch_dir(self):
        fname = self._dir
        if not os.path.exists(fname):
            os.mkdir(fname)

    def get_indicator_func(self, indicator):
        indicator = indicator.split('-')[0]    # 如果名字里面包含':'则':'后面的是需要传入的参数
        func = getattr(self._mod, indicator, None)
        if func is None:
            func = getattr(self._common_mod, indicator, None)
            if func is None:
                self.loggings.error('can`t find function %s in lib \'%s\' or \'common.py\'' % (indicator, self._mod.__name__))
        return func

    def get_indicator_value(self, indicator, argu=None):
        func = self.get_indicator_func(indicator)   

        # 根据API的参数要求传参
        args = dict()
        for name, param in inspect.signature(func).parameters.items():
            if name == 'get_oid':
                args.update(dict(get_oid = self.get_oid))
            elif name == 'walk_oid':
                args.update(dict(walk_oid = self.walk_oid))
            elif param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                if not argu is None:
                    args.update({name:argu})
                    argu = None
                else:
                    raise RuntimeError ('API: %s has one more customize argument' % indicator)

        if func is None:
            return None

        try:
            r = func(**args) if args else func()
        except Exception as e:
            self.loggings.error('API %s Error : %s' % (func.__name__, e))
            return None
        if r is None:
            return None    # func return None means unused
        if isinstance(r, tuple):
            return r
        else:
            self.loggings.error('API %s returns is not a tuple ' % func.__name__)
            return None

    def create_rrd(self, indicator):
        func = self.get_indicator_func(indicator)
        if func is None:
            return None
        if not os.path.exists(self._dir):
            self.create_switch_dir()
        kw = {
            'fname' : os.path.join(self._dir, indicator+'.rrd'),
            'DS' : getattr(func, 'DS', default['DS']),
            'step' : getattr(func, 'step', default['step']),
            'DST' : getattr(func, 'DST', default['DST']),
            'max' : getattr(func, 'max', default['max']),
            'min' : getattr(func, 'min', default['min']),
            'CF' : getattr(func, 'CF', default['CF']),
            'CDP' : getattr(func, 'CDP', default['CDP']),
            'size' : getattr(func, 'size', default['size'])
        }
        rrd_tools.create(**kw)

    def update_rrd(self, indicator, value):
        fname = os.path.join(self._dir, indicator+'.rrd')
        if not os.path.exists(fname):
            self.create_rrd(indicator)
        rrd_tools.update(fname=fname, value=value)

    def get_last_value(self, indicator):
        fname = os.path.join(self._dir, indicator+'.rrd')
        if not os.path.exists(fname):
            return None
        return [int(float(r)) for r in rrd_tools.get_last_value(fname)]

    def get_last_update(self, indicator):
        fname = os.path.join(self._dir, indicator+'.rrd')
        if not os.path.exists(fname):
            return None
        return [int(float(r)) for r in rrd_tools.get_last_update(fname)]

    def get_max_value(self, indicator):
        fname = os.path.join(self._dir, indicator+'.rrd')
        if not os.path.exists(fname):
            return None
        return [int(float(r)) for r in rrd_tools.get_max(fname)]

    def get_graph(self, indicator, **kw):
        '''
        根据指标名称和指标获取函数的装饰属性创建指示图
        '''
        func = self.get_indicator_func(indicator)
        fname = os.path.join(self._dir, indicator+'.rrd')
        # 如果该设备未定义指标获取方法或未创建RRD文件则退出
        if not os.path.exists(fname) or func is None:
            return None
        kw = {
            'title' : kw.get('title', indicator),
            'DS' : getattr(func, 'DS', default['DS']),
            'CF' : getattr(func, 'CF', default['CF']),
            'max' : getattr(func, 'max', default['max']),
            'min' : getattr(func, 'min', default['min']),
        }
        return rrd_tools.graph(fname, **kw)
        

if __name__ == '__main__':
    test = device(id=1, host='192.168.31.100', vendor='cisco', model='3640', snmp_community='public')
    print(test.get_indicator_value('IO_rate', 1))
