from coroweb import get, post
from models import *
import switch_tools
import config
import openpyxl
from io import BytesIO
import json

@get('/')
def index(**kw):
    switch_list = yield from quick_indicator.findall()
    switches = []
    for each in switch_list:
        args = {
            'id' : each['switch_id'],
            'host' : each['host'],
            'name' : each['name'],
            'cpu' : each['cpu'],
            'memory' : each['memory'],
        }
        switches.append(dict(**args))
    return {
        '__template__':'index.html',
        'switches' : switches
    }

@get('/detail')
def detail(*, swid):
    switch = yield from switches.find(pk=[swid])
    extra = yield from indicator.findall(where="`switch_id` = '%s'" % swid)
    common = config.configs.common_indicator
    indicators = [key for key, value in common.items()]
    device = switch_tools.device(**switch)

    # cpu
    if 'cpu' in indicators:
        cpu = device.get_graph('cpu', title='CPU Utilization')
    if 'memory' in indicators:
        memory = device.get_graph('memory', title='Memory Utilization')

    customize_indicator = []
    if not extra is None:
        for each in extra:
            name = each['name']
            argu = str(json.loads(each['argument']))
            kw = {}
            if not each['title'] is None:
                kw['title'] = each['title']
            customize_indicator.append(device.get_graph(name+'-'+argu, **kw))

    return {
        '__template__' : 'detail.html',
        'cpu_img' : cpu,
        'memory_img' : memory,
        'customize_indicator' : customize_indicator
    }

@get('/zb.xlsx')
def zb_xlsx():
    wb = openpyxl.Workbook()

    ws = wb.active
    table = yield from quick_indicator.findall()
    # 写入首行
    for index, value in enumerate(['管理IP', '设备名称', 'CPU利用率', '内存利用率']):
        ws.cell(row=1, column=index+1).value = value
    # 写入所有数据
    seq = ['host', 'name', 'cpu', 'memory']
    for row_index, row_value in enumerate(table):
        for col_index in range(4):
            value = row_value[seq[col_index]]
            ws.cell(row=row_index+2, column=col_index+1).value = value

    f = BytesIO()
    wb.save(f)
    return f.getvalue()
    