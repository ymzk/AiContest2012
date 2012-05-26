
from ymzkgame.manager import Manager
from ymzkgame.moveClasses import MoveByKey
from ymzkgame.gameObject import GameObject
def GetKeyEvent(current,units, debugObjects):
    i = None
    if Manager.getKeyStatus(Manager.K_0):
      i = 0
    elif Manager.getKeyStatus(Manager.K_1):
      i = 1
    elif Manager.getKeyStatus(Manager.K_2):
      i = 2
    elif Manager.getKeyStatus(Manager.K_3):
      i = 3
    elif Manager.getKeyStatus(Manager.K_4):
      i = 4
    elif Manager.getKeyStatus(Manager.K_5):
      i = 5
    elif Manager.getKeyStatus(Manager.K_6):
      i = 6
    elif Manager.getKeyStatus(Manager.K_7):
      i = 7
    elif Manager.getKeyStatus(Manager.K_8):
      i = 8
    elif Manager.getKeyStatus(Manager.K_9):
      i = 9
    elif Manager.getKeyStatus(Manager.K_s):
      result = GameObject(position = current.getPosition(), direction = -1.57079633, move = MoveByKey(speed = 5))
      while debugObjects:
        debugObjects.pop()
      debugObjects.append(result)
      return result
    if i == None:
      return current
    elif i < len(units):
      while debugObjects:
        debugObjects.pop()
      return units[i]
    else:
      return current
  
