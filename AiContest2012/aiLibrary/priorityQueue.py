
class PriorityQueue(list):
    def __init__(self, *args,
                 key = None,
                 compare = None):
        self._data = []
        if compare == None:
            if key == None:
                self._compare = lambda a, b: a < b
            else:
                self._compare = lambda a, b: key(a) < key(b)
        else:
            self._compare = compare
    def push(self, obj):
        self._data.append(obj)
        index = len(self._data) - 1
        while index != 0:
            nextIndex = (index - 1) // 2
            if self._compare(self._data[index], self._data[nextIndex]):
                self._data[index], self._data[nextIndex] = self._data[nextIndex], self._data[index]
                index = nextIndex
                continue
            break
    def pop(self):
        self._data[0], self._data[-1] = self._data[-1], self._data[0]
        result = self._data.pop()
        index = 0
        while index < len(self._data):
            left = index * 2 + 1
            if left >= len(self._data):
                break
            right = index * 2 + 2
            if right >= len(self._data) or\
               self._compare(self._data[left], self._data[right]):
                if self._compare(self._data[left], self._data[index]):
                    self._data[index], self._data[left] = self._data[left], self._data[index]
                    index = left
                    continue
            else:
                if self._compare(self._data[right], self._data[index]):
                    self._data[index], self._data[right] = self._data[right], self._data[index]
                    index = right
                    continue
            break
        return result
    def empty(self):
        return len(self._data) == 0

if __name__ == '__main__':
    queue = PriorityQueue()
    for i in range(10):
        queue.push((-2) ** i)
    for i in range(3):
        print(queue.pop())
    for i in range(10):
        queue.push((-3) ** i)
    for i in range(10):
        print(queue.pop())
