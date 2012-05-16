from checkPassable import checkPassable

def binarySearch(l, h, func):
    while h - l > 1:
        c = (l + h) // 2
        if func(c):
            h = c
        else:
            l = c
    return h

def smoothPath(field, path):
    path = list(path)
    i = 0
    while i < len(path) - 1:
        yield path[i]
        i = binarySearch(i + 1, len(path),
                         lambda a: not checkPassable(field, path[i], path[a]))
    yield path[-1]

if __name__ == '__main__':
    [print(i) for i in smoothPath(None, list(range(12)))]
