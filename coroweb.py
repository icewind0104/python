#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio, functools, inspect
from urllib import parse
from aiohttp import web
import os

def get(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__path__ = path
        wrapper.__method__ = 'GET'
        return wrapper
    return decorator

def post(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__path__ = path
        wrapper.__method__ = 'POST'
        return wrapper
    return decorator

def has_var_kw_args(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True

def has_named_kw_args(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True

def get_required_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)

def get_named_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)

def need_request_args(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if name == 'request':
            return True
    return False

class RequestHandler():
    def __init__(self, fn):
        self._func = fn

        self._has_var_kw_args = has_var_kw_args(fn)
        self._has_named_kw_args = has_named_kw_args(fn)
        self._named_kw_args = get_named_kw_args(fn)
        self._required_kw_args = get_required_kw_args(fn)
        self._need_request_args = need_request_args(fn)

    @asyncio.coroutine
    def __call__(self, request):
        kw = None
        # 如果fn需要传入参数，则先从GET和POST提取，再从request.match_info提取，并储存到kw中。
        if self._has_var_kw_args or self._has_named_kw_args:
            # 从GET中获取参数
            if request.method == 'GET':
                qs = request.query_string
                if qs:
                    kw = dict()
                    for name, param in parse.parse_qs(qs, True).items():
                        kw[name] = param[0]
            # 从POST中获取参数
            if request.method == 'POST':
                if not request.content_type:
                    return web.HTTPBadRequest('Missing Content-Type.')
                ct = request.content_type.lower()
                if ct.startswith('application/json'):
                    params = yield from request.json()
                    if isinstance(params, dict):
                        return web.HTTPBadRequest('JSON body must be object.')
                    kw = params
                elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    params = yield from request.post()
                    kw = dict(**params)
                else:
                    return web.HTTPBadRequest('Unsupported Content-Type : %s' % request.content_type)
            # 从match_info中获取参数
            if kw is None:
                kw = dict(**request.match_info)
            else:
                for name, value in request.match_info.items():
                    '''
                    if name in kw:
                        logging.warnning('duplicate param has found : %s' % name)
                    '''
                    kw[name] = value
            # 如果函数需要request作为参数，则加入request
            if self._need_request_args:
                '''
                if getattr(kw, 'request', None):
                    logging.warnning('duplicate param has found : %s' % name)
                '''
                kw['request'] = request
            # 如果函数不接受任意关键字参数(没有**kw)，则剔除无用参数
            if not self._has_var_kw_args:
                useless = []
                for key, value in kw.items():
                    if key not in self._named_kw_args:
                        useless.append(key)
                for param_name in useless:
                    kw.pop(param_name)
            # 检查必须参数是否已获取
            for name in self._required_kw_args:
                if name not in kw:
                    return web.HTTPBadRequest('Missing argument: %s' % name)
        if kw:
            r = yield from self._func(**kw)
        else:
            r = yield from self._func()
        return r
'''
        except APIError as e:
            #return web.HTTPBadRequest(e)
            return dict(error=e.error, data=e.data, message=e.message)    
''' 

def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)

def add_routers(app, model_name):
    mod = __import__(model_name, globals(), locals())
    for attr in dir(mod):
        if not attr.startswith('_'):
            fn = getattr(mod, attr)
            if callable(fn):
                path = getattr(fn, '__path__', None)
                method = getattr(fn, '__method__', None)
                if path and method:
                    fn = asyncio.coroutine(fn)
                    app.router.add_route(method, path, RequestHandler(fn))

