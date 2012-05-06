from . runnable import Runnable

class Wait(Runnable):
  def __init__(self, length):
    for base in self.__class__.__bases__:
      base.__init__(self)
    self.__length = length
  def run(self):
    for i in range(self.__length):
      yield
