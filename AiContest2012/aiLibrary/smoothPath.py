from . checkPassable import checkPassable
import sys

def binarySearch(l, h, func):
    print('start binarySearch', file = sys.stderr)
    sys.stderr.flush()
    while h - l > 1:
        c = (l + h) // 2
        if func(c):
            h = c
        else:
            l = c
    print('end binarySearch', file = sys.stderr)
    sys.stderr.flush()
    return h

def smoothPath(field, path):
    print('start smoothPath', file = sys.stderr)
    sys.stderr.flush()
    path = list(path)
    i = 0
    while i < len(path) - 1:
        yield path[i]
        i = binarySearch(i + 1, len(path),
                         lambda a: not checkPassable(field, path[i], path[a]))
    yield path[-1]
    print('end smoothPath', file = sys.stderr)
    sys.stderr.flush()

if __name__ == '__main__':
    [print(i) for i in smoothPath(None, list(range(12)))]
