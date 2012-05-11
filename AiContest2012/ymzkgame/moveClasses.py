from math import pi as PI
from . utility import EPS
from . coordinate import Coordinate
from . move import Move
from . manager import Manager

class NoMove(Move):
    def __call__(self, position, direction):
        return self, position, direction

class Set(Move):
    def __init__(self, position = None, direction = None):
        self.__targetPosition = position
        self.__targetDirection = direction
    def __call__(self, position, direction):
        if self.__targetPosition == None:
            resultPosition = position
        else:
            resultPosition = self.__targetPosition
        if self.__targetDirection == None:
            resultDirection = direction
        else:
            resultDirection = self.__targetDirection
        return NoMove(), self.__targetPosition, self.__targetDirection

class MoveTo(Move):
    def __init__(self, position = None, direction = None, term = 0):
        self.__targetPosition = position
        self.__targetDirection = direction
        self.__term = term
        self.__count = 0
    def __call__(self, position, direction):
        if self.__count >= self.__term:
            if self.__targetPosition == None:
                resultPosition = position
            else:
                resultPosition = self.__targetPosition
            if self.__targetDirection == None:
                resultDirection = direction
            else:
                resultDirection = self.__targetDirection
            return NoMove(), resultPosition, resultDirection
        else:
            if self.__targetPosition == None:
                resultPosition = position
            else:
                resultPosition = position + (self.__targetPosition - position) / (self.__term - self.__count)
            if self.__targetDirection == None:
                resultDirection = direction
            else:
                directionDiff = (self.__targetDirection - direction) % (2 * pi)
                if directionDiff < pi:
                    resultDirection = direction + directionDiff / (self.__term - self.__count)
                else:
                    resultDirection = direction - (2 * pi - directionDiff) / (self.__term - self.__count)
            self.__count += 1
            return self, resultPosition, resultDirection

class MoveStraight(Move):
    def __init__(self, velocity = None, rollVelocity = None, term = None):
        self.__velocity = velocity
        self.__rollVelocity = rollVelocity
        self.__term = term
        self.__count = 0
    def __call__(self, position, direction):
        if self.__term != None and self.__count >= self.__term:
            return NoMove(), position, direction
        if self.__velocity == None:
            resultPosition = position
        else:
            resultPosition = position + self.__velocity
        if self.__rollVelocity == None:
            resultDirection = direction
        else:
            resultDirection = direction + self.__rollVelocity
        self.__count += 1
        return self, resultPosition, resultDirection

class MoveByKey(Move):
    def __init__(self, velocity = 1):
        self._velocity = velocity
    def __call__(self, position, direction):
        dx = Coordinate(1, 0)
        dy = Coordinate(0, 1)
        d = Coordinate(0, 0)
        arg = 0
        flag = False
        if Manager.getKeyStatus(Manager.K_UP):
            d -= dy
            arg = -1.57079633
            flag = True
        if Manager.getKeyStatus(Manager.K_DOWN):
            d += dy
            arg =  1.57079633
            flag = True
        if Manager.getKeyStatus(Manager.K_LEFT):
            d -= dx
            arg = 3.14159265 - arg / 2
            flag = True
        if Manager.getKeyStatus(Manager.K_RIGHT):
            d += dx
            arg /= 2
            flag = True
        if d.norm() > EPS:
            d *= self._velocity / abs(d)
            position += d
        if flag:
            direction = arg
        return self, position, direction
