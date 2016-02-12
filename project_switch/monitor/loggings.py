import time, threading

class loggings():
    def __init__(self, location, flag=None):
        self.__location = location
        self._flag = flag

    def information(self, context):
        self.write_log(context, 'INFO')

    def error(self, context):
        self.write_log(context, 'ERROR')

    def write_log(self, context, level):
        #if lock:
        with open(self.__location, 'a') as f:
            tm = time.localtime()
            now = ('%s-%s-%s %s:%s' % (tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min))
            if self._flag is None:
                _flag = ''
            else:
                _flag = '<%s>' % self._flag
            f.write('%s %s[%s] : %s\n' % (now, _flag, level, context))
