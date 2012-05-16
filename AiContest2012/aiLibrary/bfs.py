# -*- coding: cp932 -*-
from queue import Queue

ROAD, WALL, ALLY_TERITORY, ENEMY_TERITORY = range(4)

def neighborsOf(field, position):
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0))
    for move in moves:
        candidate = (position[0] + move[0], position[1] + move[1])
        try:
            if field[candidate[0]][candidate[1]] not in (ROAD, ALLY_AREA):
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
        field::[[tile::int]] : マップ情報
                         各タイル情報は以下の値で表現する
                            0: 道(通行可能なタイル)
                            1: 壁(通行不可能なタイル)
                            2: 味方陣地(味方のみ通行可能な安全地帯)
                            3: 敵陣地(敵の安全地帯)
        tileHeight::int : タイルの高さ
        tileWidth::int : タイルの幅
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
            result = []
            while currentPosition[0] != destination[0] or currentPosition != destination[1]:
                result.append((currentPosition[0], currentPosition[1]))
                currentPosition = route[currentPosition[0]][currentPosition[1]]
            return result
        for nextPosition in getNexts(field, currentPosition):
            if visited[nextPosition[0]][nextPosition[1]]:
                continue
            queue.push(nextPosition)
            visited[nextPosition[0]][nextPosition[1]] = True
            route[nextPosition[0]][nextPosition[1]] = currentPosition
    return None
