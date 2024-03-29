# coding: cp932
# from ymzkgame import *
from ymzkgame.manager import Manager
from ymzkgame.gameObject import GameObject
from ymzkgame.coordinate import Coordinate
from aiManager import *
from bullet import Bullet

from gameConfig import *

from draw import draw
# circurated reference
# import gameManager
class Unit(GameObject):
  def __init__(self, position, direction, gameManager, teamFlag,unitId , aiManager = DefaultAiManager()):
    super().__init__(position = position, direction = direction, image = "graphics/unit" + str(teamFlag) + ".bmp")
    self._unitId = unitId
    self._startingPoint = position
    self._startingDirection = direction
    self.initialize()
    self._idForAi = 0
    self._teamFlag = teamFlag
    self._aiManager = aiManager
    self._resurrection = 0
    if aiManager == None or aiManager == "None":
      self._aiManager = DefaultAiManager()
    '''
    self._aiManager.setPosition(position)
    self._aiManager.setDirection(direction)
    '''
    self._gameManager = gameManager
  def initialize(self):
    self.setPosition(self._startingPoint)
    self.setDirection(self._startingDirection)
    self._timeNextFireing = UNIT_TIME_NEXT_FIRING
    self._term = 0
    self._hp = UNIT_DEFAULT_HP
    self._attackPower = UNIT_DEFAULT_ATTACK_POWER
  def sendEndMessage(self):
    self._aiManager.sendEndMessage(self,self._gameManager)
  def sendStartingMessage(self):
    self._aiManager.sendStartingMessage(self,self._gameManager)
  def makeBullet(self):
    self._gameManager.addBullet(Bullet(self))
    self._term = self._timeNextFireing
  def changeState(self):
    if self._hp <= 0 :
      #死んだときの処理
      self._resurrection = UNIT_RESURRECTION_COST
      self.initialize()
  def getTeamFlag(self):
    return self._teamFlag
  def damage(self, damage):
    self._hp -= damage
    self.changeState()
  def getHp(self):
    return self._hp
  def setHp(self, _hp):
    self._hp = _hp

  def getAlive(self):
    return self._resurrection <= 0
  def checkAlive(self):
    return self.getAlive()
  def getHp(self):
    return self._hp
  def getUnitId(self):
    return self.unitId
  def setAttackPower(self, _attackPower):
    self._attackPower = _attackPower
  def getAttackPower(self):
    return self._attackPower
  def sendData(self):
    #todo
    self._aiManager.writeMessage(self, self._gameManager)
    '''
    self._aiManager.setPosition(self.getPosition())
    self._aiManager.setDirection(self.getDirection())
    '''
  def recieveData(self):

    self._aiManager.step()
    self._aiManager.readMessage()

    if not self.getAlive():
      return
    if self._term <= 0:
      if self._aiManager.getFiring():
        self.makeBullet()
    d = self.getDirection()
    # print(d)
    
    # print(self.getPosition(),Coordinate(cos(d), sin(d)),self._aiManager.getMove())
    #import sys
    #sys.stdout.flush()
    self.setPosition(self.getPosition() + Coordinate(cos(d), sin(d)) * self._aiManager.getMove())
    self.setDirection(d + self._aiManager.getRotate())
  def step(self):
    if self._term > 0:
      self._term -= 1
    if self._resurrection > 0:
      self._resurrection -= 1
    self.recieveData()
    super().step()
  def end(self):
    self._aiManager.end()
    super().end()
  def encode(self):
    yield str(self._hp)
    #yield str(self._unitId)
    yield str(self._teamFlag)
    yield str(self.getPosition().getX())
    yield str(self.getPosition().getY())
    yield str(self.getDirection())
    yield str(self.getAttackPower())
    yield str(self._term)
    yield str(self._unitId)

  def draw(self, screen, viewPoint):
    draw(screen, self.getImage(), self.getPosition(), self.getDirection(),
                                  viewPoint.getPosition(), viewPoint.getDirection())
    '''
    image = self.getImage().rotate(viewPoint.getDirection() - self.getDirection())
    screen.draw(image = image,
                position = (self.getPosition() -
                            viewPoint.getPosition()
                            ).rotate(-viewPoint.getDirection()) -
                            image.getSize() / 2 +
                            Manager.getScreenSize() / 2)
    '''
