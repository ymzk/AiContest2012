# from ymzkgame import *
from ymzkgame.gameObject import GameObject
from ymzkgame.coordinate import Coordinate
from aiManager import AiManager
from bullet import Bullet
# circurated reference
# import gameManager
class Unit(GameObject):
  _SPEED = 10
  def __init__(self, position, direction, gameManager, teamFlag, aiManager):
    super().__init__(position = position, direction = direction)
    self._startingPoint = position
    self._startingDirection = direction
    self.initialize()
    self._idForAi = 0
    self._teamFlag = teamFlag
    self._aiManager = aiManager
    self._aiManager.setPosition(position)
    self._aiManager.setDirection(direction)
    self._gameManager = gameManager
  def initialize(self):
    self.setPosition(self._startingPoint)
    self.setDirection(self._startingDirection)
    self._timeNextFireing = 1
    self._term = 0
    self._hp = 100
    self._attackPower = 10
  def makeBullet(self):
    self._gameManager.addBullet(Bullet(self))
    self_timeNextFireing = self._timeNextFireing
  def changeState(self):
    if self._hp <= 0 :
      #死んだときの処理
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
  def getHp(self):
    return self._hp
  def setAttackPower(self, _attackPower):
    self._attackPower = _attackPower
  def getAttackPower(self):
    return self._attackPower
  def sendData(self):
    #todo
    self._gameManager.writeMessage(self, self._aiManager.getProcess())
    self._aiManager.setPosition(self.getPosition())
    self._aiManager.setDirection(self.getDirection())
  def recieveData(self):
    '''
    #無限ループ
    process = self._aiManager.getProcess()
    for i in process:
      pass
    '''
    if self._term <= 0:
      if self._aiManager.getFiring():
        self.makeBullet()
    distinationVector = self._aiManager.getPosition() - self.getPosition()
    if abs(distinationVector) > self._SPEED:
      distinationVector = distinationVector/abs(distinationVector) * self._SPEED
    self.setPosition(self.getPosition() + distinationVector)
    self.setDirection(self._aiManager.getDirection())
  def step(self):
    if self._term > 0:
      self._term -= 1
    self._aiManager.step()
    self.recieveData()
    self.sendData()

    super().step()
    


