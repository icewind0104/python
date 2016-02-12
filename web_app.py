#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys
sys.path.append('/home/meidl/python/project_switch/monitor')
import orm
import config
import asyncio, aiohttp
from aiohttp import web
from jinja2 import Environment, FileSystemLoader
from coroweb import add_routers, add_static


def init_jinja2(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')
    app['env'] = Environment(loader=FileSystemLoader(path))

@asyncio.coroutine
def factory(app, handler):
    @asyncio.coroutine
    def response(request):

        r = yield from handler(request)

        if isinstance(r, web.StreamResponse):
            return r

        if isinstance(r, str):
            resp = web.Response(body=r.encode('utf-8'), headers={'Content-Disposition':' attachment;filename=download.txt'})

        if isinstance(r, bytes):
            fname = request.path.split('/').pop()
            resp = web.Response(body=r, headers={'Content-Disposition':' attachment;filename=%s' % fname})

        if isinstance(r, dict):
            resp = web.Response(body=app['env'].get_template(r.pop('__template__')).render(**r).encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
        return resp

    return response

@asyncio.coroutine
def init(loop):
    yield from orm.create_pool(loop=loop, **config.configs.db)
    app = web.Application(loop=loop, middlewares=[factory])
    init_jinja2(app)
    add_static(app)
    add_routers(app, 'handlers')
    srv = yield from loop.create_server(app.make_handler(), **config.configs.server)
    print('service start - %s:%s' % (config.configs.server['host'], config.configs.server['port']))
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

