from ymzkgame.runnable import Runnable
from ymzkgame.image import Image

from gameConfig import UNIT_DEFAULT_HP, BASE_DEFAULT_HP
from gameManager import GameManager
from unitStatusViewer import UnitStatusViewer

class PlayMode(Runnable):
  def __init__(self):
    Runnable.__init__(self)
    self.gameManager = GameManager()
    self.statusViewers = [UnitStatusViewer(base, BASE_DEFAULT_HP, (700, 50 + i * 50)) for i, base in enumerate(self.gameManager.bases)] +\
                         [UnitStatusViewer(unit, UNIT_DEFAULT_HP, (700, 250 + i * 50)) for i, unit in enumerate(self.gameManager.units)]
  def step(self):
    self.gameManager.step()
    for statusViewer in self.statusViewers:
      statusViewer.step()
  def isValid(self):
    return self.gameManager.isValid()
  def draw(self, screen):
    screen.fill((0, 0, 0))
    self.gameManager.draw(Image(screen.getSurface().subsurface(((0, 0), (600, 600)))))
    for statusViewer in self.statusViewers:
      statusViewer.draw(screen)
  def end(self):
    self.gameManager.end()
    for statusViewer in self.statusViewers:
      statusViewer.end()
