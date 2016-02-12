#!/bin/usr/env python3
# -*- coding: utf-8 -*-

import pymysql
import config

def format_convert(config):
    cf = config.copy()
    cf.pop('maxsize')
    cf.pop('minsize')
    cf['passwd'] = cf['password']
    cf.pop('password')
    return cf

def select(sql):
    cf = format_convert(config.configs.db)
    try:
        conn = pymysql.connect(**cf)
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        r = cur.fetchall()
        return r
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()

def insert(sql):
    cf = format_convert(config.configs.db)
    try:
        conn = pymysql.connect(**cf)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()

def exists(table, where):
    cf = format_convert(config.configs.db)
    try:
        conn = pymysql.connect(**cf)
        cur = conn.cursor()
        cur.execute('select count(*) from %s where %s' % (table, where))
        res = cur.fetchone()
        r = False if res[0] == 0 else True
        return r 
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()

def update(sql):
    cf = format_convert(config.configs.db)
    try:
        conn = pymysql.connect(**cf)
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        conn.commit()
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()
