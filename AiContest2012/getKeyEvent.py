
from ymzkgame.manager import Manager
def GetKeyEvent(current,units,special):
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
      special.setPosition(current.getPosition())
      special.setDirection(current.getDirection())
      return special
    if i == None:
      return current
    elif i < len(units):
      return units[i]
    else:
      return current
  
