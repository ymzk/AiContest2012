from ymzkgame.runnable import Runnable
from ymzkgame.gameObject import GameObject
from ymzkgame.runner import run
from ymzkgame.manager import Manager
from ymzkgame.image import Image
from playMode import PlayMode

class Menu(GameObject):
  def __init__(self):
    GameObject.__init__(self, image = Image('graphics/title.bmp', permeate = False), position = (400, 300))
  def step(self):
    GameObject.step(self)
    if any(Manager.getKeyStatus(key) for key in (Manager.K_SPACE,
                                                 Manager.K_z)):
      return PlayMode()

if __name__ == '__main__':
  run(Menu())
