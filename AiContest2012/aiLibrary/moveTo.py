from math import sin, cos
from aStar import aStar
from smoothPath import smoothPath

EPS = 1e-6

def index(field, position):
    return (position[0] / field.cellWidth, position[1] / field.cellHeight)

def addPP(a, b):
    return (a[0] + b[0], a[1] + b[1])
def subPP(a, b):
    return (a[0] - b[0], a[1] - b[1])
def mulNP(n, p):
    return (n * p[0], n * p[1])
def mulPN(p, n):
    return mulNP(n, p)
def dotPP(a, b):
    return a[0] * b[0] + a[1] * b[1]
def crossPP(a, b):
    return a[0] * b[1] - a[1] * b[0]
def normP(p):
    return p[0] * p[0] + p[1] * p[1]
def absP(p):
    return normP(p) ** (1 / 2)
def distancePP(a, b):
    return absP(subPP(a, b))

def distancePS(p, s):
    if dotPP(subPP(s[1], s[0]), subPP(position, s[0])) < -EPS:
        return distancePP(position, s[0])
    elif dotPP(subPP(s[0], s[1]), subPP(position, s[1])) < -EPS:
        return distancePP(position, s[1])
    else:
        return crossPP(subPP(s[1], s[0]), subPP(position, s[0])) / distancePP(s[0], s[1])
def distanceSP(s, p):
    return distancePS(p, s)

def getUnitVector(direction):
    return (cos(direction), sin(direction))
def unit(vector):
    return vector / absP(vector)

def cost(path, position, direction):
    return min(distancePS(position, s) for s in path) -\
           max(dotPP(getUnitVector(direction), unit(subPP(s[1], s[0])) for s in path))

SPEED = 10
ROLL_SPEED = 10

def straight(position, direction):
    return (addPP(position, mulNP(SPEED, getUnitVector(direction))), direction)
def rollRight(position, direction):
    direction -= ROLL_SPEED
    return straight(position, direction)
def rollLeft(position, direction):
    direction += ROLL_SPEED
    return straight(position, direction)

candidates = [straight, rollRight, rollLeft]

def moveTo(self, field, target):
    if (self.position, self.direction, target) == moveTo._lastArgument:
        path = smoothPath(field, aStar(field, index(self.position), index(target)))
        path = list(zip(path, path[1:]))
        moveTo._lastArgument = (self.position, self.direction, target)
    return min(candidate(position, direction) for candidate in candidates,
               key = lambda a: cost(a))
