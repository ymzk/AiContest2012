
def binarySearch(l, h, func):
    while h - l > 1:
        c = (l + h) // 2
        if func(c):
            h = c
        else:
            l = c
    return h
