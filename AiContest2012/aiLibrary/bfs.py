# -*- coding: cp932 -*-
from . queue import Queue

''' unchecked '''

def neighborsOf(field, position):
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0))
    for move in moves:
        candidate = (position[0] + move[0], position[1] + move[1])
        try:
            if field.isPassable(candidate[0], candidate[1]):
                continue
            yield candidate
        except IndexError:
            pass

def bfs(field, source, destination, getNexts = neighborsOf):
    '''
        幅優先探索によってfield上でsourceからdestinationに移動する経路を見つける関数
        経路上のマスの座標のリストを返すので、
        一度だけ実行し、その通りに移動するようにするとよい
        ※到達できない場合はNoneを返すのでチェックすること！
        各引数は以下の値を受け取る
        field::Field
        position::(y::float, x::float) : 自ユニットのfield上でのインデックス
        target::(y::float, x::float) : 移動先のfield上でのインデックス
        ※position、targetは座標をそのまま渡さないように！
    '''
    source, destination = destination, source
    queue = Queue()
    visited = [[False for j in i] for i in field]
    route = [[None for j in i] for i in field]
    queue.push(source)
    visited[source[0]][source[1]] = True
    while not queue.empty():
        currentPosition = queue.pop()
        if currentPosition[0] == destination[0] and currentPosition[1] == destination[1]:
            while currentPosition[0] != destination[0] or currentPosition != destination[1]:
                yield (currentPosition[0], currentPosition[1])
                currentPosition = route[currentPosition[0]][currentPosition[1]]
            return
        for nextPosition in getNexts(field, currentPosition):
            if visited[nextPosition[0]][nextPosition[1]]:
                continue
            queue.push(nextPosition)
            visited[nextPosition[0]][nextPosition[1]] = True
            route[nextPosition[0]][nextPosition[1]] = currentPosition
    return RuntimeError('no path is found')
