import pygame
from ymzkgame.runnable import Runnable, StopRunning
import ymzkgame.defaults as defaults
from ymzkgame.manager import Manager
from ymzkgame._keyData import KeyData

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
  def step(self):
    while True:
      if len(self.__scenes) == 0:
        return False
      try:
        tmp = self.__scenes[-1].step()
        if not isinstance(tmp, Runnable):
          break
        self.__scenes.append(tmp.setup())
      except StopRunning:
        self.__scenes.pop()
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
