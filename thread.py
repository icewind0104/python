#!/usr/bin/python3

import threading

class thread_runner():
    def __init__(self, tasks, threads=0):
        self._tasks = tasks
        self._threads = threads if threads else len(tasks)
        self._res = [None] * len(tasks)
        self._lock = threading.Lock()

    def _handler(self, i):
        while True:
            self._lock.acquire()
            try:
                c = len(self._tasks)
                if c:
                    task = self._tasks.pop()
                else:
                    return None
            finally:
                self._lock.release()
            args = task['args']
            r = task['func'](**args)
            self._res[c-1] = r

    def run(self):
        T = [None] * self._threads
        for i in range(self._threads):
            T[i] = threading.Thread(target=self._handler, args=(i,))
            T[i].start()
        for i in range(self._threads):
            T[i].join()
        return self._res
