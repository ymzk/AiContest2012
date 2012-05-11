from math import sin, cos

class Coordinate:
  def __init__(self, *args):
    if len(args) == 0:
      self.__x, self.__y = None, None
    elif len(args) == 2:
      self.__x, self.__y = args
    elif len(args) == 1:
      if hasattr(args[0], 'getX') and hasattr(args[0], 'getY'):
        self.__x = args[0].getX()
        self.__y = args[0].getY()
      elif hasattr(args[0], '__iter__'):
        self.__x, self.__y = args[0]
      elif hasattr(args[0], 'x') and hasattr(args[0], 'y'):
        self.__x = args[0].x
        self.__y = args[0].y
      else:
        raise TypeError('failed to convert Coordinate')
    else:
      raise TypeError('Coordinate() takes 0 to 2 arguments')
  def getX(self):
    return self.__x
  def getY(self):
    return self.__y
  def __repr__(self):
    return '(' + repr(self.getX()) + ', ' + repr(self.getY()) + ')'
  def __pos__(self):
    return Coordinate(self.getX(), self.getY())
  def __neg__(self):
    return Coordinate(-self.getX(), -self.getY())
  def __add__(self, other):
    return Coordinate(self.getX() + other.getX(), self.getY() + other.getY())
  def __sub__(self, other):
    return self + -other
  def __mul__(self, other):
    if isinstance(other, Coordinate):
      raise TypeError('unsupported operand type(s) for +: \'Coordinate\' and \'Coordinate\'')
    return Coordinate(self.getX() * other, self.getY() * other)
  def __rmul__(self, other):
    return Coordinate(other * self.getX(), other * self.getY())
  def __div__(self, other):
    return Coordinate(self.getX() / other, self.getY() / other)
  def __truediv__(self, other):
    return Coordinate(self.getX() / other, self.getY() / other)
  def __floordiv__(self, other):
    return Coordinate(self.getX() // other, self.getY() // other)
  def norm(self):
    return self.getX() ** 2 + self.getY() ** 2
  def __abs__(self):
    return self.norm() ** (1 / 2)
  def rotate(self, angle = 0):
    return Coordinate(self.getX() * cos(angle) - self.getY() * sin(angle),
                      self.getX() * sin(angle) + self.getY() * cos(angle))
