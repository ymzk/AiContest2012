from math import sin, cos
from . aStar import aStar
from . smoothPath import smoothPath
import sys

EPS = 1e-6

def index(field, position):
    return (position[0] / field.cellwidth, position[1] / field.cellheight)

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
           max(dotPP(getUnitVector(direction), unit(subPP(s[1], s[0]))) for s in path)

SPEED = 10
ROLL_SPEED = 10

def simurate(position, direction, speed, roll):
  direction += roll
  position = addPP(position, mulNP(speed, getUnitVector(direction)))
  return position, direction

candidates = [(10, 0, 0), (10, 0.1, 0), (10, -0.1, 0)]

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
    get(self, unit) :
      次にするべき行動を(speed, direction, fire)のタプルで返すメソッド。
      ※このクラスは移動するだけで、fireは常にFalseが返る。
        攻撃したいなら戻り値を解析すること。
      unitには自機(Unitのインスタンス)を渡す。
  '''
  def __init__(self, field, unit, target):
    self.target = target
    self.path = aStar(field, index(field, unit.position), index(field, target))
    self.path = list(smoothPath(field, self.path))
    self.path = [(t[0] * field.cellwidth, t[1] * field.cellheight) for t in zip(self.path, self.path[1:])]
    print(self.path, file = sys.stderr)
  def get(self, unit):
    return min(candidates,
               key = lambda candidate: cost(self.path, *simurate(unit.position, unit.direction, candidate[0], candidate[1])))
