import pygame
from ymzkgame.runnable import Runnable
import ymzkgame.defaults as defaults
from ymzkgame.manager import Manager
from ymzkgame._keyData import KeyData
import time

class Runner:
  def __init__(self, firstScene, title = defaults.DEFAULT_TITLE,
                                 screenSize = defaults.DEFAULT_SCREEN_SIZE,
                                 fps = defaults.DEFAULT_FPS):
    if not isinstance(firstScene, Runnable):
      raise TypeError('a Runnable is required')
    self.__scenes = [firstScene.setup()]
    self.__title = title
    self.__screenSize = screenSize
    self.__fps = fps
    self.__lastTime = None
    self.__bps = None
    self.__bpsCount = 0
  def step(self):
    print('bps:', self.__bps)
    currentTime = int(time.time())
    if currentTime != self.__lastTime:
      self.__bps = self.__bpsCount
      self.__bpsCount = 0
      self.__lastTime = currentTime
    self.__bpsCount += 1
    while True:
      while len(self.__scenes) > 0 and not self.__scenes[-1].isValid():
        self.__scenes.pop()
      if len(self.__scenes) == 0:
        return False
      tmp = self.__scenes[-1].step()
      if not isinstance(tmp, Runnable):
        break
      self.__scenes.append(tmp.setup())
    return True
  def run(self):
    pygame.init()
    pygame.display.set_caption(self.__title)
    pygame.display.set_mode(self.__screenSize)
    clock = pygame.time.Clock()
    try:
      while self.step():
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            del self.__scenes[:]
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
