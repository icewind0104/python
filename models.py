#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import config
from orm import Model, StringFeild, IntegerFeild

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
    switch_id		= IntegerFeild()
    host		= StringFeild()
    name		= StringFeild()
    cpu			= StringFeild()
    memory		= StringFeild()
