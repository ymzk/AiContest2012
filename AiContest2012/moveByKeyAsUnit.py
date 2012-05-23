from math import *

from ymzkgame.coordinate import Coordinate
from ymzkgame.manager import Manager
from ymzkgame.move import Move
class MoveByKeyAsUnit(Move):
    def __init__(self, angle = 0.2,velocity = 1):
        self._velocity = velocity
        self._angle = angle
    def __call__(self, position, direction):
        if Manager.getKeyStatus(Manager.K_UP):
            position += Coordinate(cos(direction),sin(direction)) * self._velocity
        if Manager.getKeyStatus(Manager.K_z):
            pass
        if Manager.getKeyStatus(Manager.K_LEFT):
            direction -= self._angle
        if Manager.getKeyStatus(Manager.K_RIGHT):
            direction += self._angle
        return self, position, direction
