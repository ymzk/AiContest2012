from coordinate import Coordinate
from runner import run
from manager import Manager
from image import Image
from runnable import Runnable, StopRunning
from runnableClasses import *
from move import Move
from moveClasses import *
import defaults
from gameObject import GameObject

class RunnableList(list, Runnable):
  def __init__(self, *args):
    if len(args) == 1 and hasattr(args[0], '__iter__'):
      iterable = args[0]
    else:
      iterable = args
    for base in self.__class__.__bases__:
      base.__init__(self)
    self.extend(iterable)
  def step(self):
    if len(self) == 0:
      raise StopRunning
    i = 0
    while i < len(self):
      try:
        print(i, self)
        self[i] = self[i].setup()
        self[i].step()
        i += 1
      except StopRunning:
        del self[i]

class Hoge(Runnable):
  def run(self):
    obj = GameObject()
    obj.setMove(MoveTo(Coordinate(800, 600), 180))
    for i in range(180):
      yield
      obj.step()
    yield Wait(60)

run(Hoge())
