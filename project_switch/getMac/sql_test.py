#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect('/home/meidl/python/test.db')
cur = conn.cursor()

cur.execute("select * from mac")
rs = cur.fetchall()

with open('/home/meidl/python/project_switch/getMac/table', 'w') as f:
    f.write('')
    for each in rs:
        f.write(('seq:%s, mac:%s, switch:%s, date:%s\r\n' % (each[0], each[1], each[2], each[3])))

