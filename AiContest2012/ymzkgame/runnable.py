from . import utility

class Runnable(object):
  def __init__(self, iterable = None):
    self.__iterable = iterable
    self.__finished = False
  def setup(self):
    result = self.run()
    if isinstance(result, Runnable):
      return result
    else:
      return Runnable(result)
  def run(self):
    return self
  def step(self):
    if self.__iterable == None:
      raise NotImplementedError('Runnable.run or Runnable.step must be implemented')
    try:
      return next(self.__iterable)
    except StopIteration:
      self.end()
  def draw(self, screen):
    pass
  def end(self):
    self.__finished = True
  def isValid(self):
    return not self.__finished
