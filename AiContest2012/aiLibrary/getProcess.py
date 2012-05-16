
def getProcess(source, destination):
    '''
        sourceからdestinationへ移動する時に通る座標のリストを得る関数
    '''
    diff = (destination[0] - source[0], destination[1] - source[1])
    if diff[0] < diff[1]:
        x, y = source
        dx, dy = (i / abs(i) for i in diff)
        c = 0
        dc = abs(diff[0])
        mc = abs(diff[1])
        while y != destination[1]:
            y += dy
            yield (x, y)
            c += dc
            if c >= mc:
                x += dx
                c -= mc
                yield (x, y)
    else:
        x, y = source
        dx, dy = (i / abs(i) for i in diff)
        c = 0
        dc = abs(diff[1])
        mc = abs(diff[0])
        while x != destination[0]:
            x += dx
            yield (x, y)
            c += dc
            if c >= mc:
                y += dy
                c -= mc
                yield (x, y)

if __name__ == '__main__':
    for p in getProcess((0, 0), (30, 13)):
        print(p)
