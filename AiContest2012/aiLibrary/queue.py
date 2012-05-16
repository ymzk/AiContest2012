
class Queue:
    def __init__(self):
        self._data = []
    def push(self, obj):
        self._data.append(obj)
    def pop(self):
        return self._data.pop(0)
    def empty(self):
        return bool(self._data)
