#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import sys
import os
from orm import Model, StringFeild, IntegerFeild, select

class left_join():
    def __init__(self, class_list):
        table = []
        for cls in class_list:
            table.append(cls.__name__)

        column = []    # 生成包含所有CLS属性的列表，形如:[`tabname`.`column1`, `tabname`.`column2`, ...]
        for cls in class_list:
            primary_key	= '`%s`.`%s`' % (cls.__name__, cls.__primary_key__)
            feilds	= ['`%s`.`%s`' % (cls.__name__, column) for column in cls.__feilds__]
            column.extend([primary_key] + feilds)

        relations = []
        '''
        查找所有表间连接关系，生成列表: [{'tableName1':'column', 'tableName2':'column'}, ...]
        '''
        for cls in class_list:
            for each in cls.__foreign_key__:    # forerign_key 格式 (self_column, foreign_column, foreign_table)
                self_tabal = cls.__table__
                self_column, foreign_column, foreign_table = each
                relations.append({self_tabal:self_column, foreign_table:foreign_column})

        queue = []
        '''
        表间关系进行排序，所有传入的class即table，必须满足每一张表都唯一与前面某一张表存在连接关系，
        并将这些关系按传入表顺序排序。
        '''
        for index, cls in enumerate(class_list[1:]):    # 从第二个元素开始
            found = False				# 只能找到一个关系，多个则报错
            for before_cls in class_list[:index+1]:     # 遍历该表之前的所有表，查找连接关系
                for relation in relations:              # 遍历连接关系，查找两张表间是否存在连接
                    if cls.__name__ in relation and before_cls.__name__ in relation:
                        if found == False:
                            queue.append(relation)      # 将连接关系推入队列
                            found = True
                        else:
                            raise RuntimeError ('found one more relationship between %s and %s' % ([x.__name__ for x in class_list[:index+1]], cls.__name__))
                        break
            else:
                if found == False:
                    raise RuntimeError ('There is no relationship between %s and %s' % ([x.__name__ for x in class_list[:index+1]], cls.__name__))

        # 构建select语句
        select = 'SELECT %s ' % (','.join(column))
        select += 'FROM `%s` ' % (class_list[0].__name__)
        for i in range(1,len(class_list)):    # 从第二个开始
            joined_tab, joined_col = class_list[i].__name__, queue[i-1].pop(class_list[i].__name__)
            join_tab, join_col = queue[i-1].popitem()
            select += 'LEFT JOIN `%s` ON `%s`.`%s`=`%s`.`%s` ' % (joined_tab, join_tab, join_col, joined_tab, joined_col)

        self.__select__ = select

    @asyncio.coroutine
    def findall(self, where=None, order=None, args=None):
        sql = self.__select__
        if not where is None:
            sql += ' WHERE '
            sql += where
        if not order is None:
            sql += ' ORDER BY '
            sql += order
        r = yield from select(sql, args)
        return r

class switches(Model):
    __table__		= 'switches'
    id			= IntegerFeild(primary_key=True, auto_increment=True)
    vendor		= StringFeild()
    model		= StringFeild()
    host		= StringFeild()
    user		= StringFeild()
    password		= StringFeild()
    supassword		= StringFeild()
    snmp_community	= StringFeild()
    snmp_version	= IntegerFeild()

class indicator(Model):
    __table__		= 'indicator'
    id			= IntegerFeild(primary_key=True, auto_increment=True)
    switch_id		= IntegerFeild()
    name		= StringFeild()
    argument		= StringFeild()
    title		= StringFeild()

class quick_indicator(Model):
    __table__		= 'quick_indicator'
    id			= IntegerFeild(primary_key=True, auto_increment=True)
    switch_id		= IntegerFeild(foreign_key=('id', 'switches'))
    host		= StringFeild()
    name		= StringFeild()
    cpu			= StringFeild()
    memory		= StringFeild()

class switches_groups(Model):
    __table__		= 'switches_groups'
    id			= IntegerFeild(primary_key=True, auto_increment=True)
    switch_id		= IntegerFeild(foreign_key=('id', 'switches'))
    group_id		= IntegerFeild(foreign_key=('id', 'groups'))

class groups(Model):
    __table__		= 'groups'
    id			= IntegerFeild(primary_key=True, auto_increment=True)
    name		= StringFeild()
    priority		= IntegerFeild()
    category_id		= IntegerFeild(foreign_key=('id', 'category'))

class category(Model):
    __table__		= 'category'
    id			= IntegerFeild(primary_key=True, auto_increment=True)
    name		= StringFeild()
