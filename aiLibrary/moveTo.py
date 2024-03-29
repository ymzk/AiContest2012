# coding: cp932
import sys
from math import sin, cos
from . aStar import aStar
from . smoothPath import smoothPath
from . binarySearch import binarySearch
from . checkPassable import checkPassable
from . index import index
from gameConfig import UNIT_MAX_SPEED, UNIT_MAX_ROLL_ANGLE, FIELD_CELL_WIDTH, FIELD_CELL_HEIGHT

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

def simulate(position, direction, speed, roll):
  direction += roll
  position = addPP(position, mulNP(speed, getUnitVector(direction)))
  return position, regularizeAngle(direction)

candidates = [(UNIT_MAX_SPEED, 0, 0), (UNIT_MAX_SPEED, UNIT_MAX_ROLL_ANGLE, 0), (UNIT_MAX_SPEED, -UNIT_MAX_ROLL_ANGLE, 0)]

class MoveTo:
  '''
    座標で指定された位置へ移動する為の入力を生成するクラス。
    コンストラクタに現在地と目的地を渡すとルートを検索し、
    その結果を繰り返し使用して移動する。
    このクラスの戻り値を無視して移動した後再びこのクラスを利用しようとすると、
    元のルートに戻そうとするため、新しいオブジェクトを作った方がいいかもしれない。
    但し、コンストラクタの計算が重いため、繰り返し計算すると速度低下の原因になる。
    __init__(self, field, unit, target):
      コンストラクタ。
      fieldにはフィールド情報(Fieldのインスタンス)を、
      unitには自機(Unitのインスタンス)を、
      targetには２要素(x, y)のタプル(Unit.positionでも可)を渡す。
    get(self, field, unit):
      次にするべき行動を(speed, direction, fire)のタプルで返すメソッド。
      ※このクラスは移動するだけで、fireは常にFalseが返る。
        攻撃したいなら戻り値を解析すること。
      unitには自機(Unitのインスタンス)を渡す。
  '''
  def __init__(self, field, unit, target):
    self.target = target
    self.path = [(p[0] * FIELD_CELL_WIDTH + FIELD_CELL_WIDTH // 2, p[1] * FIELD_CELL_HEIGHT + FIELD_CELL_HEIGHT // 2) for p in aStar(field, index(field, unit.position), index(field, target))]
#    print(self.path, file = sys.stderr)
#    sys.stderr.flush()
    self.path = list(smoothPath(field, self.path))
#    print(self.path, file = sys.stderr)
#    sys.stderr.flush()
    self.path = list(zip(self.path, self.path[1:]))
  def get(self, field, unit):
    return min(candidates,
               key = lambda candidate: cost(field, self.path, *simulate(unit.position, unit.direction, candidate[0], candidate[1])))
