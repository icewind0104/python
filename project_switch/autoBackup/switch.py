#!/usr/bin/python3

import threading, pexpect, re, math, time

#========================= cisco ===========================

class switch_cisco():
    def __init__(self, ip, user, passwd, supasswd, *var, **kw):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.supasswd = supasswd
        self.name = ''
        self.__timeOut = 30
        #print('ip:%s,user:%s,passwd:%s,supasswd:%s' % (self.ip,self.user,self.passwd,self.supasswd))

    def getInfo(self, info=None):
        result = {}
        child = pexpect.spawn('telnet '+self.ip)
        try:
            self.login(child)
            for each in info:
                result[each] = self.getOutput(child, each)
            self.logout(child)
        except Exception as e:
            return {'error':e}
        finally:
            self.logout(child)
        return result

    def excute(self, cmd_list):
        cmd_sum = len(cmd_list)
        child = pexpect.spawn('telnet '+self.ip)
        try:
            self.login(child)
        except Exception:
            #print('login error !')
            return 0
        for index, each_cmd in enumerate(cmd_list):
            #print('log: %s' % each_cmd)
            try:
                self.__excute(child, each_cmd)
            except Exception:
                #print('%s/%s CMD excute error !' % (index, cmd_sum))
                return index
        self.logout(child)
        return None

    def __excute(self, child, each_cmd):
        child.sendline(each_cmd)
        child.expect(self.name+'#', timeout=self.__timeOut)

    def getOutput(self, child, cmd):
        outPut = ''
        child.sendline(cmd)
        try:
            I = child.expect([self.name+'#', ' --More-- '], timeout=self.__timeOut)
        except Exception:
            raise RuntimeError ('CMD error : (output) %s' % child.before)
        outPut += child.before.decode('utf-8')
        if I != 0:
            while True:
                child.send(' ')
                try:
                    i = child.expect([self.name+'#', ' --More-- '], timeout=self.__timeOut)
                except Exception:
                    raise RuntimeError ('CMD error : (output) %s' % child.before)
                outPut += child.before.decode('utf-8')[26:]
                if i == 0:
                    break
        return outPut

    def login(self, child):
        if self.user:
            try:
                child.expect(['Username', 'login:'], timeout=self.__timeOut)
            except Exception:
                raise RuntimeError ('connection error : (output) %s' % child.before)
            child.sendline(self.user)
        try:
            child.expect(['password', 'Password:'], timeout=self.__timeOut)
        except:
            raise RuntimeError ('connection error : (output) %s' % child.before)
        child.sendline(self.passwd)
        try:
            child.expect('>', timeout=self.__timeOut)
        except Exception:
            raise RuntimeError ('login_error: (output) %s' % child.before)
        self.name = re.search('\n(.*)',child.before.decode('utf-8')).group(1)
        child.sendline('enable')
        if self.supasswd:
            child.expect(['password', 'Password:'], timeout=self.__timeOut)
            child.sendline(self.supasswd)
        try:
            child.expect(self.name+'#', timeout=self.__timeOut)
        except Exception:
            raise RuntimeError ('login_error: (output) %s' % child.before)
       
        return None

    def logout(self, child):
        child.sendline('quit')

#======================= huawei =========================

class switch_huawei():
    def __init__(self, ip, user, passwd, supasswd, *var, **kw):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.supasswd = supasswd
        self.name = ''
        self.__timeOut = 30
        #print('ip:%s,user:%s,passwd:%s,supasswd:%s' % (self.ip,self.user,self.passwd,self.supasswd))

    def getInfo(self, info=None):
        result = {}
        child = pexpect.spawn('telnet '+self.ip)
        try:
            self.login(child)
            for each in info:
                result[each] = self.getOutput(child, each)
            self.logout(child)
        except Exception as e:
            return {'error':e}
        finally:
            self.logout(child)
        return result

    def excute(self, cmd_list):
        cmd_sum = len(cmd_list)
        child = pexpect.spawn('telnet '+self.ip)
        try:
            self.login(child)
        except Exception:
            #print('login error !')
            return 0
        for index, each_cmd in enumerate(cmd_list):
            #print('log: %s' % each_cmd)
            try:
                self.__excute(child, each_cmd)
            except Exception:
                #print('%s/%s CMD excute error !' % (index, cmd_sum))
                return index
        self.logout(child)
        return None

    def __excute(self, child, each_cmd):
        child.sendline(each_cmd)
        child.expect('<'+self.name+'>', timeout=self.__timeOut)

    def getOutput(self, child, cmd):
        outPut = ''
        child.sendline(cmd)
        try:
            i = child.expect(['<'+self.name+'>', '  ---- More ----'], timeout=self.__timeOut)
        except Exception:
            raise RuntimeError ('CMD error : (output) %s' % child.before)
        outPut += child.before.decode('utf-8')
        if i == 1:
            while True:
                child.send(' ')
                try:
                    i = child.expect(['<'+self.name+'>', '  ---- More ----'], timeout=self.__timeOut)
                except Exception:
                    raise RuntimeError ('CMD error : (output) %s' % child.before)
                outPut += child.before.decode('utf-8')[52:]
                if i == 0:
                    break
        return outPut

    def login(self, child):
        if self.user:
            try:
                child.expect('Username:', timeout=self.__timeOut)
            except Exception:
                raise RuntimeError ('connection error : (output) %s' % child.before)
            child.sendline(self.user)
        try:
            child.expect('Password:', timeout=self.__timeOut)
        except:
            raise RuntimeError ('connection error : (output) %s' % child.before)
        child.sendline(self.passwd)
        try:
            child.expect('>', timeout=self.__timeOut)
        except Exception:
            raise RuntimeError ('login_error: (output) %s' % child.before)
        self.name = re.search('<(.*)$',child.before.decode('utf-8')).group(1)
        if self.supasswd:
            child.sendline('super')
            child.expect('Password:', timeout=self.__timeOut)
            child.sendline(self.supasswd)
            try:
                child.expect('<'+self.name+'>', timeout=self.__timeOut)
            except Exception:
                raise RuntimeError ('login_error: (output) %s' % child.before)
        return None

    def logout(self, child):
        child.sendline('quit')

#========================= maipu ===========================

class switch_maipu():
    def __init__(self, ip, user, passwd, supasswd, *var, **kw):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.supasswd = supasswd
        self.name = ''
        self.__timeOut = 30
        #print('ip:%s,user:%s,passwd:%s,supasswd:%s' % (self.ip,self.user,self.passwd,self.supasswd))

    def getInfo(self, info=None):
        result = {}
        child = pexpect.spawn('telnet '+self.ip)
        try:
            self.login(child)
            for each in info:
                result[each] = self.getOutput(child, each)
            self.logout(child)
        except Exception as e:
            return {'error':e}
        finally:
            self.logout(child)
        return result

    def excute(self, cmd_list):
        cmd_sum = len(cmd_list)
        child = pexpect.spawn('telnet '+self.ip)
        try:
            self.login(child)
        except Exception:
            #print('login error !')
            return 0
        for index, each_cmd in enumerate(cmd_list):
            #print('log: %s' % each_cmd)
            try:
                self.__excute(child, each_cmd)
            except Exception:
                #print('%s/%s CMD excute error !' % (index, cmd_sum))
                return index
        self.logout(child)
        return None

    def __excute(self, child, each_cmd):
        child.sendline(each_cmd)
        child.expect(self.name+'#', timeout=self.__timeOut)

    def getOutput(self, child, cmd):
        outPut = ''
        child.sendline(cmd)
        try:
            I = child.expect([self.name+'#', ' --More-- ', '---More---'], timeout=self.__timeOut)
        except Exception:
            raise RuntimeError ('CMD error : (output) %s' % child.before)
        outPut += child.before.decode('utf-8')
        if I != 0:
            while True:
                child.send(' ')
                try:
                    i = child.expect([self.name+'#', ' --More-- ', '---More---'], timeout=self.__timeOut)
                except Exception:
                    raise RuntimeError ('CMD error : (output) %s' % child.before)
                outPut += child.before.decode('utf-8')[[30,19][I-1]:]
                if i == 0:
                    break
        return outPut

    def login(self, child):
        if self.user:
            try:
                child.expect(['Username', 'login:'], timeout=self.__timeOut)
            except Exception:
                raise RuntimeError ('connection error : (output) %s' % child.before)
            child.sendline(self.user)
        try:
            child.expect(['password', 'Password:'], timeout=self.__timeOut)
        except:
            raise RuntimeError ('connection error : (output) %s' % child.before)
        child.sendline(self.passwd)
        try:
            child.expect('>', timeout=self.__timeOut)
        except Exception:
            raise RuntimeError ('login_error: (output) %s' % child.before)
        self.name = re.search('\n(.*)',child.before.decode('utf-8')).group(1)
        child.sendline('enable')
        if self.supasswd:
            child.expect(['password', 'Password:'], timeout=self.__timeOut)
            child.sendline(self.supasswd)
        try:
            child.expect(self.name+'#', timeout=self.__timeOut)
        except Exception:
            raise RuntimeError ('login_error: (output) %s' % child.before)
       
        return None

    def logout(self, child):
        child.sendline('quit')

#===========================================================


def getSW(Path, device_ip=None):
    SW = []
    with open(Path) as openFile:
        innerContext = openFile.readlines()
        for each in innerContext[1:]:
            L = each[:-1].split(':')
            vendor = L[0]
            ip = L[1]
            user = L[2] if L[2] else None
            passwd = L[3] if L[3] else None
            supasswd = L[4] if L[4] else None
            save_path = L[5]
            if device_ip and not (ip in device_ip):
                continue
            SW.append({
                'vendor':vendor,
                'ip':ip,
                'user':user,
                'passwd':passwd,
                'supasswd':supasswd,
                'save_path':save_path
            })
        return SW

class threadRunner():
    def __init__(self, tasks):
        self.tasks = tasks
        self.result = [None]*len(tasks)
        self.T = [None]*len(tasks)

    def trace_func(self, func, args, seq):
        res = func(**args)
        self.result[seq] = res

    def run(self):
        for index, each in enumerate(self.tasks):
            self.T[index] = threading.Thread(target=self.trace_func, args=(each['func'], each['args'], index))
            self.T[index].start()
        for each in self.T:
            each.join()

        return self.result

#==================== logging ===================
class logging():
    def __init__(self, location):
        self.__location = location

    def information(self, context):
        self.write_log(context, 'INFO')

    def error(self, context):
        self.write_log(context, 'ERROR')

    def write_log(self, context, level):
        with open(self.__location, 'a') as f:
            tm = time.localtime()
            now = ('%s-%s-%s %s:%s' % (tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min))
            f.write('%s [%s] : %s\n' % (now, level, context))
