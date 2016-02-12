#!/usr/bin/env python3
# -*- coding : utf-8 -*-

import aiomysql
import asyncio

@asyncio.coroutine
def create_pool(loop, **kw):
    global __pool
    __pool = yield from aiomysql.create_pool(
        host = kw.get('host', '127.0.0.1'),
        port = kw.get('port', 3306),
        user = kw['user'],
        password = kw['password'],
        db = kw['db'],
        autocommit = kw.get('autocommit', True),
        charset = kw.get('charset', 'utf8'),
        maxsize = kw.get('maxsize', 10),
        minsize = kw.get('minsize', 1),
        loop = loop)
    return __pool

@asyncio.coroutine
def select(sql, args, size=None):
    global __pool
    with (yield from __pool) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
        yield from cur.close()
        return rs

@asyncio.coroutine
def execute(sql, args):
    global __pool
    with (yield from __pool) as conn:
        cur = yield from conn.cursor()
        yield from cur.execute(sql.replace('?', '%s'), args or ())
        affected = cur.rowcount
        yield from cur.close()
    return affected

#================= Feild ==================

class Feild(object):
    def __init__(self, name, column_type, primary_key, default, auto_increment=False):
        self.name		= name
        self.column_type	= column_type
        self.primary_key	= primary_key
        self.default		= default
        self.auto_increment	= auto_increment

    def __str__(self):
        return '%s,%s:%s' % (self.__class__.__name__, self.column_type, self.name)


class StringFeild(Feild):
    def __init__(self, ddl='varchar(50)', name=None, primary_key=False, default=None, auto_increment=False):
        super().__init__(name, ddl, primary_key, default, auto_increment)

class IntegerFeild(Feild):
    def __init__(self, ddl='integer', name=None, primary_key=False, default=None, auto_increment=False):
        super().__init__(name, ddl, primary_key, default, auto_increment)

#================= Meta class ====================

class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)

        tableName	= attrs.get('__table__', None) or name
        #print("Model_log : found table name : %s" % tableName)

        mappings	= {}
        feilds		= []
        primary_key	= None
        unInc_feilds	= []
        for key, value in attrs.items():
            if isinstance(value, Feild):
                #print("Model_log : found Feild : %s" % value.name)
                mappings[key] = value
                if not value.auto_increment:
                    unInc_feilds.append(key)
                if value.primary_key:
                    if primary_key:
                        raise RuntimeError('Duplicate primary key for fieild : %s' & key)
                    primary_key = key
                else:
                    feilds.append(key)

        if not primary_key:
            raise RuntimeError('primary key not found')

        for key in mappings:
            attrs.pop(key)

        escaped_feilds			= list(map(lambda f : '`%s`' % f, feilds))
        escaped_unInc_feilds		= list(map(lambda f : '`%s`' % f, unInc_feilds))
        attrs['__table__']		= tableName
        attrs['__mappings__']		= mappings
        attrs['__feilds__']		= feilds
        attrs['__unInc_feilds__']	= unInc_feilds
        attrs['__primary_key__']	= primary_key
        attrs['__select__']		= 'select `%s`,%s from `%s`' % (primary_key, ','.join(escaped_feilds), tableName)
        attrs['__insert__']		= 'insert into %s (%s) values (%s)' % (tableName, ','.join(escaped_unInc_feilds), ','.join(['?']*len(unInc_feilds)))

        return type.__new__(cls, name, bases, attrs)

#================= Model ===================

class Model(dict, metaclass=ModelMetaClass):

    def __init__(self, **kw):
        super(Model, self).__init__(kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute %s" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return self.get(key, None)

    def getValueOrDefault(self, key):
        value = self.get(key, None)
        if value is None:
            feild = self.__mappings__[key]
            if feild.default is not None:
                value = feild.default() if callable(feild.default) else feild.default
                #print("Model_log : use default value %s - %s" % (key, str(value)))
            self[key] = value
        return value

    @classmethod
    @asyncio.coroutine
    def find(cls, pk):
        sql = ('%s where `%s`=?' % (cls.__select__, cls.__primary_key__))
        rs = yield from select(sql, [pk])
        return cls(**rs[0])

    @classmethod
    @asyncio.coroutine
    def findall(cls, where=None, args=[]):
        sql = cls.__select__
        if where:
           sql += ' where '
           sql += where
        rs = yield from select(sql, args)
        return rs

    @asyncio.coroutine
    def save(self):
        args = list(map(self.getValueOrDefault, self.__unInc_feilds__))
        rows = yield from execute(self.__insert__, args)
        if rows != 1:
            raise RuntimeError ('failed to insert record: affected rows: %s' % rows)

