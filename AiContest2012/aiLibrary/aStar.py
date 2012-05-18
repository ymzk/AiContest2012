# -*- coding: cp932 -*-
from . priorityQueue import PriorityQueue
import sys

_INF = float('inf')
_EPS = 1e-6

def aroundOf(field, position):
    moves = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    for move in moves:
        candidate = (int(position[0] + move[0]), int(position[1] + move[1]))
        try:
            if not field.isPassable(position[1], candidate[0])or\
               not field.isPassable(candidate[1], position[0]) or\
               not field.isPassable(candidate[1], candidate[0]):
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
    source = (int(source[0]), int(source[1]))
    destination = (int(destination[0]), int(destination[1]))
    queue = PriorityQueue(key = lambda state: state[2])
    memo = [[_INF for j in i] for i in field.fielddata]
    route = [[None for j in i] for i in field.fielddata]
    queue.push((source, 0, 0 + distance(source, destination)))
    while not queue.empty():
        currentState = queue.pop()
        currentPosition = currentState[0]
        currentCost = currentState[1]
        currentEstimation = currentState[2]
        if currentPosition[0] == destination[0] and currentPosition[1] == destination[1]:
            while currentPosition[0] != source[0] or currentPosition[1] != source[1]:
                yield currentPosition
                currentPosition = route[currentPosition[1]][currentPosition[0]]
            return
        if memo[currentPosition[1]][currentPosition[0]] < currentEstimation - _EPS:
            continue
        for nextPosition in getNexts(field, currentState[0]):
            nextCost = currentCost + getCost(currentPosition, nextPosition)
            nextEstimation = nextCost + estimateFunction(nextPosition, destination)
            if memo[nextPosition[1]][nextPosition[0]] < nextEstimation + _EPS:
                continue
            queue.push((nextPosition,
                        nextCost,
                        nextEstimation))
            memo[nextPosition[1]][nextPosition[0]] = nextEstimation
            route[nextPosition[1]][nextPosition[0]] = currentPosition
    raise RuntimeError('no path is found')
