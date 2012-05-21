# coding: cp932
import sys
from math import sin, cos
from . aStar import aStar
from . smoothPath import smoothPath
from . binarySearch import binarySearch
from . checkPassable import checkPassable
from . index import index

INF = float('inf')
EPS = 1e-6

def addPP(a, b):
    return (a[0] + b[0], a[1] + b[1])
def subPP(a, b):
    return (a[0] - b[0], a[1] - b[1])
def mulNP(n, p):
    return (n * p[0], n * p[1])
def mulPN(p, n):
    return mulNP(n, p)
def divPN(p, n):
    return (p[0] / n, p[1] / n)
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
    if dotPP(subPP(s[1], s[0]), subPP(p, s[0])) < EPS:
        return distancePP(p, s[0])
    elif dotPP(subPP(s[0], s[1]), subPP(p, s[1])) < EPS:
        return distancePP(p, s[1])
    else:
        return abs(crossPP(subPP(s[1], s[0]), subPP(p, s[0]))) / distancePP(s[0], s[1])
def distanceSP(s, p):
    return distancePS(p, s)

def getUnitVector(direction):
    return (cos(direction), sin(direction))
def unit(vector):
    return divPN(vector, absP(vector))
def regularizeAngle(angle):
  return (angle%(6.2831853)+3.14159265)%(6.2831853)-3.14159265

def cost(field, path, position, direction):
#    result =  min(distancePS(position, s) - dotPP(getUnitVector(direction), 10 * unit(subPP(s[1], position))) for s in path)
    if len(path) <= 0:
        return INF
    target = min((i for i in path), key = lambda s: distancePS(position, s) - 10 * dotPP(getUnitVector(direction), unit(subPP(s[1], position))))
#    print(position, getUnitVector(direction), file = sys.stderr)
#    print(target, file = sys.stderr)
    distance = distancePS(position, target)
    alternation = 10 * dotPP(getUnitVector(direction), unit(subPP(target[1], position)))
#    print('distance=', distance, 'alternation=', alternation, file = sys.stderr)
    result = distance - alternation
#    print(result, file = sys.stderr)
#    sys.stderr.flush()
    return result

SPEED = 10
ROLL_SPEED = 10

def simurate(position, direction, speed, roll):
  direction += roll
  position = addPP(position, mulNP(speed, getUnitVector(direction)))
  return position, regularizeAngle(direction)

candidates = [(10, 0, 0), (10, 0.1, 0), (10, -0.1, 0)]

class MoveTo:
  '''
    ���W�Ŏw�肳�ꂽ�ʒu�ֈړ�����ׂ̓��͂𐶐�����N���X�B
    �R���X�g���N�^�Ɍ��ݒn�ƖړI�n��n���ƃ��[�g���������A
    ���̌��ʂ��J��Ԃ��g�p���Ĉړ�����B
    ���̃N���X�̖߂�l�𖳎����Ĉړ�������Ăт��̃N���X�𗘗p���悤�Ƃ���ƁA
    ���̃��[�g�ɖ߂����Ƃ��邽�߁A�V�����I�u�W�F�N�g�����������������������Ȃ��B
    �A���A�R���X�g���N�^�̌v�Z���d�����߁A�J��Ԃ��v�Z����Ƒ��x�ቺ�̌����ɂȂ�B
    __init__(self, field, unit, target):
      �R���X�g���N�^�B
      field�ɂ̓t�B�[���h���(Field�̃C���X�^���X)���A
      unit�ɂ͎��@(Unit�̃C���X�^���X)���A
      target�ɂ͂Q�v�f(x, y)�̃^�v��(Unit.position�ł���)��n���B
    get(self, field, unit):
      ���ɂ���ׂ��s����(speed, direction, fire)�̃^�v���ŕԂ����\�b�h�B
      �����̃N���X�͈ړ����邾���ŁAfire�͏��False���Ԃ�B
        �U���������Ȃ�߂�l����͂��邱�ƁB
      unit�ɂ͎��@(Unit�̃C���X�^���X)��n���B
  '''
  def __init__(self, field, unit, target):
    self.target = target
    self.path = list(aStar(field, index(field, unit.position), index(field, target)))
#    print(self.path, file = sys.stderr)
#    sys.stderr.flush()
    self.path = [(p[0] * field.cellWidth + field.cellWidth // 2, p[1] * field.cellHeight + field.cellHeight // 2) for p in smoothPath(field, self.path)]
#    print(self.path, file = sys.stderr)
#    sys.stderr.flush()
    self.path = list(zip(self.path, self.path[1:]))
  def get(self, field, unit):
    return min(candidates,
               key = lambda candidate: cost(field, self.path, *simurate(unit.position, unit.direction, candidate[0], candidate[1])))
