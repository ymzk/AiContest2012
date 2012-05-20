
def getProcess(source, destination):
    '''
        sourceからdestinationへ移動する時に通る座標のリストを得る関数
    '''
    diff = (destination[0] - source[0], destination[1] - source[1])
    if abs(diff[0]) < abs(diff[1]):
        x, y = source
        if abs(diff[0]) > 0:
            dx = diff[0] // abs(diff[0])
        if abs(diff[1]) > 0:
            dy = diff[1] // abs(diff[1])
        dc = abs(diff[0])
        mc = abs(diff[1])
        c = mc // 2
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
        if abs(diff[0]) > 0:
            dx = diff[0] // abs(diff[0])
        if abs(diff[1]) > 0:
            dy = diff[1] // abs(diff[1])
        dc = abs(diff[1])
        mc = abs(diff[0])
        c = mc // 2
        while x != destination[0]:
            x += dx
            yield (x, y)
            c += dc
            if c >= mc:
                y += dy
                c -= mc
                yield (x, y)

if __name__ == '__main__':
    for p in getProcess((15, 6), (16, 33)):
        print(p)
