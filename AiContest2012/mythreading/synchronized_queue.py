from threading import Lock

class SynchronizedQueue:
    def __init__(self, maxSize = -1):
        self._lock = Lock()
        self._data = []
        self._maxSize = maxSize
    def push(self, obj):
        if self.full():
            return False
        self._lock.acquire()
        try:
            self._data.append(obj)
        finally:
            self._lock.release()
        return True
    def pop(self):
        if self.empty():
            return False, None
        self._lock.acquire()
        try:
            result = self._data.pop(0)
        finally:
            self._lock.release()
        return True, result
    def noWaitPush(self, obj):
        if self._lock.acquire(blocking = False):
            try:
                if self.full():
                    return False
                self._data.append(obj)
            finally:
                self._lock.release()
            return True
        else:
            return False
    def noWaitPop(self):
        if self._lock.acquire(blocking = False):
            if self.empty():
                return False, None
            try:
                result = self._data.pop(0)
            finally:
                self._lock.release()
            return True, result
        else:
            return False, None
    def empty(self):
        return len(self._data) == 0
    def full(self):
        return len(self._data) == self._maxSize
    def clear(self):
        self._lock.acquire()
        try:
            self._data = []
        finally:
            self._lock.release()
