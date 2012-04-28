import ymzkgame.utility

class StopRunning(Exception):
  pass

class Runnable(object):
  def __init__(self, iterable = None):
    self.__iterable = iterable
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
      raise StopRunning()
  def end(self):
    raise StopRunning()
