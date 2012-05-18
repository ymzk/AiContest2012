from math import *

from ymzkgame.coordinate import Coordinate
from ymzkgame.manager import Manager
from ymzkgame.move import Move
class MoveByKeyAsUnit(Move):
    def __init__(self, velocity = 1):
        self._velocity = velocity
    def __call__(self, position, direction):
        if Manager.getKeyStatus(Manager.K_UP):
            position += Coordinate(cos(direction),sin(direction)) * self._velocity
        if Manager.getKeyStatus(Manager.K_z):
            pass
        if Manager.getKeyStatus(Manager.K_LEFT):
            direction -= 0.2
        if Manager.getKeyStatus(Manager.K_RIGHT):
            direction += 0.2
        return self, position, direction
