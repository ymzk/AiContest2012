from threading import Lock

class SynchronizedFile:
    def __init__(self, file):
        self._file = file
        self._lock = Lock()
    def close(self):
        self._file.close()
    def flush(self):
        self._file.flush()
    def fileno(self):
        return self._file.fileno()
    def isatty(self):
        return self._file.isatty()
    def __next__(self):
        return next(self._file)
    def read(size = None):
        self._lock.acquire()
        try:
            if size == None:
                return self._file.read()
            else:
                return self._file.read(size)
        finally:
            self._lock.release()
    def readline(self, size = None):
        self._lock.acquire()
        try:
            if size == None:
                return self._file.readline()
            else:
                return self._file.readline(size)
        finally:
            self._lock.release()
    def readlines(self, size = None):
        self._lock.acquire()
        try:
            if size == None:
                return self._file.readlines()
            else:
                return self._file.readlines(size)
        finally:
            self._lock.release()
    def write(self, message):
        self._lock.acquire()
        try:
            self._file.write(message)
        finally:
            self._lock.release()
