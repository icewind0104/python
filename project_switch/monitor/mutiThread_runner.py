#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading

class mutiThread():
    def __init__(self, task_pool, threads=1):
        self._task_pool = task_pool
        self._threads = int(threads)
        self._res = [None] * len(task_pool)
        self._lock = threading.Lock()

    def _handler(self):
        while True:
            self._lock.acquire()
            try:
                c = len(self._task_pool)
                if c:
                    task = self._task_pool.pop()
                else:
                    break
            finally:
                self._lock.release()
            func = task['func']
            args = task['args']
            if args is None:
                self._res[c-1] = func()
            else:
                if isinstance(args, dict):
                    self._res[c-1] = func(**args)
                else:
                    raise ValueError ('task_pool`s args must be a dict')

    def run(self):
        T = [None] * self._threads
        for i in range(self._threads):
            T[i] = threading.Thread(target=self._handler)
            T[i].start()
        for i in range(self._threads):
            T[i].join()
        return self._res
