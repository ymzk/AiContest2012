
class Coordinate:
  def __init__(self, *args):
    if len(args) == 0:
      self.x, self.y = None, None
    elif len(args) == 2:
      self.x, self.y = args
    else:
      raise TypeError('Coordinate() takes 0 or 2 arguments')
  def __repr__(self):
    return '(' + repr(self.x) + ', ' + repr(self.y) + ')'
  def __pos__(self):
    return Coordinate(self.x, self.y)
  def __neg__(self):
    return Coordinate(-self.x, -self.y)
  def __add__(self, other):
    return Coordinate(self.x + other.x, self.y + other.y)
  def __sub__(self, other):
    return self + -other
  def __mul__(self, other):
    if isinstance(other, Coordinate):
      raise TypeError('unsupported operand type(s) for +: \'Coordinate\' and \'Coordinate\'')
    return Coordinate(self.x * other, self.y * other)
  def __rmul__(self, other):
    return Coordinate(other * self.x, other * self.y)
  def __div__(self, other):
    return Coordinate(self.x / other, self.y / other)
  def __truediv__(self, other):
    return Coordinate(self.x / other, self.y / other)
  def __floordiv__(self, other):
    return Coordinate(self.x // other, self.y // other)
