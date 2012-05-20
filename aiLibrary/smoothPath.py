from . checkPassable import checkPassable
import sys
from . binarySearch import binarySearch

def smoothPath(field, path):
    path = list(path)
    i = 0
    while i < len(path) - 1:
        yield path[i]
        i = binarySearch(i + 1, len(path),
                         lambda a: not checkPassable(field, path[i], path[a])) - 1
    yield path[-1]

if __name__ == '__main__':
    [print(i) for i in smoothPath(None, list(range(12)))]
