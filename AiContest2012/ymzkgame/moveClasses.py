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
    UNIT_VECTOR_X = Coordinate(1, 0)
    UNIT_VECTOR_Y = Coordinate(0, 1)
    def __init__(self, speed = 1):
        self._speed = speed
    def __call__(self, position, direction):
        velocity = Coordinate(0, 0)
        if Manager.getKeyStatus(Manager.K_UP):
            velocity -= self.UNIT_VECTOR_Y
        if Manager.getKeyStatus(Manager.K_DOWN):
            velocity += self.UNIT_VECTOR_Y
        if Manager.getKeyStatus(Manager.K_LEFT):
            velocity -= self.UNIT_VECTOR_X
        if Manager.getKeyStatus(Manager.K_RIGHT):
            velocity += self.UNIT_VECTOR_X
        if velocity.norm() > EPS:
            velocity /= abs(velocity)
        velocity *= self._speed
        return self, position + velocity, direction
