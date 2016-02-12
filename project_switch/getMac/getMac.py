#!/usr/local/python
# -*- coding utf-8 -*-

import math, re, string, switch, time, sqlite3, os
from switch import logging

# create IP list
class IP():
    def __init__(self, IP_str):
        self.ip = re.match('(([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3}))/([0-9]{1,2})', IP_str)
        if not self.ip:
            raise RuntimeError('%s is not a legal IP address' % IP_str)
        for each in range(2,6):
            if int(self.ip.group(each)) > 255:
                raise RuntimeError('%s is not a legal IP address' % IP_str)

        self.ip_addr = self.ip.group(1)
        self.__A = self.ip.group(2)
        self.__B = self.ip.group(3)
        self.__C = self.ip.group(4)
        self.__D = self.ip.group(5)
        self.__A_bin = bin(int(self.__A))[2:].rjust(8,'0')
        self.__B_bin = bin(int(self.__B))[2:].rjust(8,'0')
        self.__C_bin = bin(int(self.__C))[2:].rjust(8,'0')
        self.__D_bin = bin(int(self.__D))[2:].rjust(8,'0')
        self.Mask = int(self.ip.group(6))
        self.IP_bin = self.__A_bin + self.__B_bin + self.__C_bin + self.__D_bin
        self.IP_bin_net = self.IP_bin[:self.Mask].ljust(32,'0')

    def getHosts(self):
        num = 2**(32-self.Mask)-1
        Mask_A = math.floor(num / 256**3)
        num = num % 256**3
        Mask_B = math.floor(num / 256**2)
        num = num % 256**2
        Mask_C = math.floor(num / 256**1)
        num = num % 256**1
        Mask_D = num %256

        IP_net_A = int(self.IP_bin_net[0:8], 2)
        IP_net_B = int(self.IP_bin_net[8:16], 2)
        IP_net_C = int(self.IP_bin_net[16:24], 2)
        IP_net_D = int(self.IP_bin_net[24:32], 2)

        Hosts = []
        part = [None]*4
        for a in range(0, Mask_A + 1):
            part[0] = str(IP_net_A + a)
            for b in range(0, Mask_B + 1):
                part[1] = str(IP_net_B + b)
                for c in range(0, Mask_C + 1):
                    part[2] = str(IP_net_C + c)
                    for d in range(0, Mask_D + 1):
                        part[3] = str(IP_net_D + d)
                        Hosts.append('.'.join(part))
        return Hosts[1:-1]

#================== creat ARP ====================

def creatARP(SW, ip_list):
    
    sw = switch.switch(**SW[0])
    threads = 4

    splited_list = split(ip_list,threads)
    # 将IP数组平均分割为 n 组，n = 线程数

    tasks = [{'func':fping, 'args':{'sw':sw,'ip_list':each}} for each in splited_list]
    # 将函数与需要参与计算的参数打包进 tasks

    thread_runner = switch.threadRunner(tasks)
    res = thread_runner.run()

    is_succ = True
    for index, each in enumerate(res):    #检查执行是否有错
        if each != None:
            logging.error('Thread-%s/%s execute "ping" command failed at index %s' % (index+1, thread, each))
            is_succ = False
    
    if is_succ == False:
        raise RuntimeError

'''
    while True:
        splited_list = split(ip_list,threads)
        tasks = [{'func':fping, 'args':{'sw':sw,'ip_list':each}} for each in splited_list]
        thread_runner = switch.threadRunner(tasks)
        result = thread_runner.run()
        ip_list.clear()
        for each in result:
            if not each == None:
                ip_list.extend(each)
        if len(ip_list) != 0:
            if YesOrNo(('There are %s IP failed, do you want to try again' % len(ip_list))):
                continue
        else:
            print('create ARP successful !')
            break      
'''

def fping(sw, ip_list):
    cmd = ['ping -t 200 -c 1 '+x for x in ip_list]
    error_order = sw.excute(cmd)
    if not error_order == None:
        return ip_list[error_order:]
    else:
        return None

def split(L, parts):
    result = []
    for i in range(0, parts):
        result.append(L[i::parts])
    return result

def YesOrNo(context='please input [yes/no]'):
    while True:
        choose = input(context).lower()
        if choose in ['y','n','yes','no']:
            break
        else:
            print('input error !')
            time.sleep(1)
    if choose in ['y','yes']:
        return True
    if choose in ['n','no']:
        return False

#=================== get ARP =======================
def getARP(SW):
    sw = switch.switch(**SW[0])
    result = sw.getInfo(['dis arp'])

    if result.get('error', None):
        raise RuntimeError (result['error'])

    return result

'''
    while True:
        sw = switch.switch(**SW[0])
        try:
            result = sw.getInfo(['dis arp'])
        except Exception:
            if YesOrNo('Some error has occured, try again [yes/no]?'):
                continue
        break
    return result
'''

#=================== get MacTable ====================
def get_mac_table(SW):
    tasks = [{'func':get_output_mac_table, 'args':each} for each in SW]
    thread_runner = switch.threadRunner(tasks)
    result = thread_runner.run()

    output_list = []
    is_succ = True
    for index, each in enumerate(result):
        if not each.get('error', None):
            output_list.append(each['dis mac dy'])
        else:
            loggin.error(each['error'])
            is_succ = False

    if is_succ == False:
        raise RuntimeError

    return output_list

'''
    while True:
        thread_runner = switch.threadRunner(tasks)
        result = thread_runner.run()
        output_list = []
        failed_list = []
        for index, each in enumerate(result):
            if not each.get('error', None):
                output_list.append(each['dis mac dy'])
            else:
                print('log: error - %s' % each['error'])
                failed_list.append(tasks[index])
        if len(failed_list) == 0:
            break
        else:
            if YesOrNo('There are %s task(s) failed when get mac table, do you want try again [yes/no] ? ' % len(failed_list)):
                tasks = failed_list
                continue
            else:
                break
    return output_list
'''

def get_output_mac_table(**kw):
    sw = switch.switch(**kw)
    return sw.getInfo(['dis mac dy'])

#================= save ==================
def has_exists(mac, cur):

    mac_addr = mac['mac']
    switch = mac['ip']

    cur.execute("select count(*) from mac where mac='%s' and switch='%s'" % (mac_addr, switch))
    #print("select * from mac where mac='%s' and switch='%s'" % (mac_addr, switch))
    res = cur.fetchone()

    if res[0] == 1:
        #print(res[0])
        return True
    elif res[0] == 0:
        return False
    else:
        raise RuntimeError ('log: Unknown error occured when check mac whether exists')

def sql_update(mac, conn):

    mac_addr = mac['mac']
    switch = mac['ip']
    datetime = mac['datetime']

    conn.execute("UPDATE mac SET datetime='%s' where mac='%s' and switch='%s'" % (datetime, mac_addr, switch))
    #print("UPDATE mac SET datetime='%s' where mac='%s' and switch='%s'" % (datetime, mac_addr, switch))

def sql_insert(mac, conn):

    mac_addr = mac['mac']
    switch = mac['ip']
    datetime = mac['datetime']

    conn.execute("INSERT INTO mac(mac,switch,datetime) VALUES ('%s','%s','%s')" % (mac_addr, switch, datetime))
    #print("INSERT INTO mac(mac,switch,datetime) VALUES ('%s','%s','%s')" % (mac_addr, switch, datetime))
    logging.information("INSERT INTO mac(mac,switch,datetime) VALUES ('%s','%s','%s')" % (mac_addr, switch, datetime))





#====================== main ========================

logging = logging('/home/meidl/python/project_switch/getMac/log')
logging.information('Begin')

# check network
logging.information('checking network ...')

output = os.popen('ping -c 3 10.189.46.1').read()
if not re.findall('64 bytes from', output):
    logging.error('network check failed')
    logging.information('Program exit.\n')
    exit()

date = time.localtime()
datetime = ('%s-%s-%s %s:%s:%s' % (date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour,date.tm_min, date.tm_sec))

Path = '/home/meidl/python/project_switch/autoBackup/switches.txt'

Switches = switch.getSW(Path, device_ip='10.189.46.9')

#============== step 1 create ARP ==================

logging.information('Creating ARP ...')

try:
    creatARP(Switches, IP('10.189.20.0/23').getHosts())
except Exception:
    logging.information('Program exit.\n')
    exit()

#============== step 2 get wireless MAC ==================

logging.information('Getting wireless MAC ...')

try:
    arp_info = getARP(Switches)['dis arp']
except Exception as e:
    logging.error(e)
    logging.information('Program exit.\n')
    exit()

mac_wireless_list = re.findall('10.189.2[01].[0-9]{1,3}[ ]*([0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4})[ ]*.*[ ]*GigabitEthernet0/0/15', arp_info)
#get all mac

mac_count = len(mac_wireless_list)
# get count of mac

mac_wireless_list = list(set(mac_wireless_list))
# delete duplicate element

mac_count_no_dup = len(mac_wireless_list)
# get count of maces (no dup)

mac_wireless_list = [{'mac':x, 'ip':Switches[0]['ip'], 'datetime':datetime} for x in mac_wireless_list]

logging.information('%s(%s) wireless mac find' % (mac_count_no_dup, mac_count))

#============== step 3 get Ethernet MAC =================

logging.information('Getting Ethernet MAC ...')

ip_list = ['10.189.46.66','10.189.46.7','10.189.46.8','10.189.46.9','10.189.46.10']
Switches = switch.getSW(Path, device_ip=ip_list)

try:
    mac_table_list = get_mac_table(Switches)
except Exception:
    logging.information('Program exit.\n')
    exit()

mac_eth_list = []
#print(mac_table_list[4])
for index, each in enumerate(mac_table_list):
    mac_list = re.findall('[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}', each)
    #get all mac

    mac_count = len(mac_list)
    # get count of mac

    mac_list = list(set(mac_list))
    # delete duplicate element

    mac_count_no_dup = len(mac_list)
    # get count of mac (no dup)

    mac_list = [{'mac':x, 'ip':ip_list[index], 'datetime':datetime} for x in mac_list]

    logging.information('%s(%s) eth mac find at %s' % (mac_count_no_dup, mac_count, ip_list[index]))

    mac_eth_list.extend(mac_list)

#============== step 4 
all_mac_list = mac_eth_list + mac_wireless_list

#============== step 5 save into database =================

logging.information('saving into database ...')

Database = '/home/meidl/python/test.db'

conn = sqlite3.connect(Database)
cur = conn.cursor()

count_update = 0
count_insert = 0

for each in all_mac_list:
    if has_exists(each, cur):
        sql_update(each, conn)
        count_update += 1
    else:
        sql_insert(each, conn)
        count_insert += 1

conn.commit()
cur.close()
conn.close()

logging.information('save complete - %s has update, %s has insert' % (count_update, count_insert))
logging.information('End\n')
