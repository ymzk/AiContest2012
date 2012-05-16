# -*- coding: cp932 -*-
from priorityQueue import PriorityQueue

_INF = float('inf')
_EPS = 1e-6

def aroundOf(field, position):
    moves = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    for move in moves:
        candidate = (position[0] + move[0], position[1] + move[1])
        try:
            if not field.isPassable(position[0], candidate[1])or\
               not field.isPassable(candidate[0], position[1]) or\
               not field.isPassable(candidate[0], candidate[1]):
                continue
            yield candidate
        except IndexError:
            pass

def distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2)

def aStar(field, source, destination, getNexts = aroundOf, getCost = distance, estimateFunction = distance):
    '''
        A*アルゴリズムによってfield上でsourceからdestinationに移動する経路を見つける関数
        壁の少ないマップでは、幅優先探索と比べてより最短に近い経路を出力する
        グリッド上での探索の結果を平滑化するならこちらの方がお勧め
        引数、戻り値はbfsを参照
    '''
    source, destination = destination, source
    queue = PriorityQueue(key = lambda state: state[2])
    memo = [[_INF for j in i] for i in field]
    route = [[None for j in i] for i in field]
    queue.push((source, 0, 0 + distance(source, destination)))
    while not queue.empty():
        currentState = queue.pop()
        currentPosition = currentState[0]
        currentCost = currentState[1]
        currentEstimation = currentState[2]
        if currentPosition[0] == destination[0] and currentPosition[1] == destination[1]:
            while currentPosition[0] != destination[0] or currentPosition[1] != destination[1]:
                yield (currentPosition[0] * tileHeight, currentPosition[1] * tileWidth)
                currentPosition = route[currentPosition[0]][currentPosition[1]]
            return
        if memo[currentPosition[0]][currentPosition[1]] < currentEstimation - _EPS:
            continue
        for nextPosition in getNexts(currentState[0]):
            nextCost = currentCost + getCost(currentPosition, nextPosition)
            nextEstimation = nextCost + estimateFunction(nextPosition, destination)
            if memo[nextPosition[0]][nextPosition[1]] < nextEstimation + _EPS:
                continue
            queue.push((nextPosition,
                        nextCost,
                        nextEstimation))
            memo[nextPosition[0]][nextPosition[1]] = nextEstimation
            route[nextPosition[0]][nextPosition[1]] = currentPosition
    raise RuntimeError('no path is found')
