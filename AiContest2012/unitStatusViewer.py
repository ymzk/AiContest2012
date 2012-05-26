from ymzkgame.gameObject import GameObject
from ymzkgame.runnable import Runnable
from ymzkgame.runnableList import RunnableList
from ymzkgame.runner import run
from ymzkgame.coordinate import Coordinate
from ymzkgame.image import Image

class LifeBar(RunnableList):
  class Bar(Runnable):
    def __init__(self, unit, maxHp, position = Coordinate(0, 0)):
      Runnable.__init__(self)
      self.image = Image('graphics/lifeBar.bmp', permeate = False)
      self.imageSize = self.image.getSize()
      self.position = Coordinate(position)
      self.unit = unit
      self.maxHp = maxHp
    def step(self):
      pass
    def draw(self, screen):
      ration = self.unit.getHp() / self.maxHp
#      print(ration, self.position)
      if ration < 0:
        ration = 0
      if ration > 1:
        ration = 1
      screen.draw(self.image.getSubImage((0, 0), (self.imageSize.getX() * ration, self.imageSize.getY())), self.position - self.imageSize / 2)
  def __init__(self, unit, maxHp, position):
    RunnableList.__init__(self)
    self.append(GameObject(image = 'graphics/lifeBox.bmp', position = position))
    self.append(self.Bar(unit, maxHp, position))

class UnitStatusViewer(RunnableList):
  def __init__(self, unit, maxHp, position = Coordinate(0, 0)):
    RunnableList.__init__(self)
    self.unit = unit
    self.position = Coordinate(position)
    unitImage = unit.getImage()
    self.append(GameObject(image = unitImage,
                           position = self.position - Coordinate(60, 0)))
    self.append(LifeBar(unit, maxHp, self.position + Coordinate(20, 0)))

if __name__ == '__main__':
  unit = GameObject(image = Image('lifeBar.bmp', permeate = False))
  unit.hp = 80
  run(UnitStatusViewer(unit, 100, (400, 300)))
