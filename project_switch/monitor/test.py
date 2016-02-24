#!/usr/bin/python3

import switch_tools
import db

switches = db.select('select * from switches')

for switch in switches:
    device = switch_tools.device(**switch)
    switch_id = device.id
    name = device.get_indicator_value('name')
    db.update("update switches set `name` = '%s' where `id` = %s" % (name[0], switch_id))

