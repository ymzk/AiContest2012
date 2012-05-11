import time
import pygame
from . runnable import Runnable
from . import defaults
from . manager import Manager
from . _keyData import KeyData
from . utility import toTuple
from . coordinate import Coordinate

class Runner:
  def __init__(self, firstScene, title = defaults.DEFAULT_TITLE,
                                 screenSize = defaults.DEFAULT_SCREEN_SIZE,
                                 fps = defaults.DEFAULT_FPS):
    if not isinstance(firstScene, Runnable):
      raise TypeError('a Runnable is required')
    self.__scenes = [firstScene.setup()]
    self.__title = title
    self.__screenSize = Coordinate(screenSize)
    self.__fps = fps
    self.__lastTime = None
    self.__bps = None
    self.__bpsCount = 0
  def step(self):
    currentTime = int(time.time())
    if currentTime != self.__lastTime:
      self.__bps = self.__bpsCount
      self.__bpsCount = 0
      self.__lastTime = currentTime
    self.__bpsCount += 1
    print('bps:', self.__bps)
    while True:
      while len(self.__scenes) > 0 and not self.__scenes[-1].isValid():
        self.__scenes.pop()
      if len(self.__scenes) == 0:
        return False
      tmp = self.__scenes[-1].step()
      self.__scenes[-1].draw(Manager.getScreen())
      if not isinstance(tmp, Runnable):
        break
      self.__scenes.append(tmp.setup())
    return True
  def run(self):
    pygame.init()
    pygame.display.set_caption(self.__title)
    pygame.display.set_mode(toTuple(self.__screenSize))
    assert pygame.display.get_init()
    clock = pygame.time.Clock()
    try:
      while self.step():
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            for scene in self.__scenes[::-1]:
              scene.end()
            print(self.__scenes)
          elif event.type == pygame.KEYDOWN:
            KeyData.setKeyStatus(event.key, True)
          elif event.type == pygame.KEYUP:
            KeyData.setKeyStatus(event.key, False)
          elif event.type == pygame.MOUSEMOTION:
            KeyData.setMousePosition(event.pos)
        pygame.display.flip()
        clock.tick(self.__fps)
    finally:
      pygame.quit()

def run(firstScene, title = defaults.DEFAULT_TITLE,
                    screenSize = defaults.DEFAULT_SCREEN_SIZE,
                    fps = defaults.DEFAULT_FPS):
  Runner(firstScene, title, screenSize, fps).run()
