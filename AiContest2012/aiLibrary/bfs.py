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
        ���D��T���ɂ����field���source����destination�Ɉړ�����o�H��������֐�
        �o�H��̃}�X�̍��W�̃��X�g��Ԃ��̂ŁA
        ��x�������s���A���̒ʂ�Ɉړ�����悤�ɂ���Ƃ悢
        �����B�ł��Ȃ��ꍇ��None��Ԃ��̂Ń`�F�b�N���邱�ƁI
        �e�����͈ȉ��̒l���󂯎��
        field::[[tile::int]] : �}�b�v���
                         �e�^�C�����͈ȉ��̒l�ŕ\������
                            0: ��(�ʍs�\�ȃ^�C��)
                            1: ��(�ʍs�s�\�ȃ^�C��)
                            2: �����w�n(�����̂ݒʍs�\�Ȉ��S�n��)
                            3: �G�w�n(�G�̈��S�n��)
        tileHeight::int : �^�C���̍���
        tileWidth::int : �^�C���̕�
        position::(y::float, x::float) : �����j�b�g��field��ł̃C���f�b�N�X
        target::(y::float, x::float) : �ړ����field��ł̃C���f�b�N�X
        ��position�Atarget�͍��W�����̂܂ܓn���Ȃ��悤�ɁI
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
