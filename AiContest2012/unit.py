# from ymzkgame import *
from ymzkgame.gameObject import GameObject
from ymzkgame.coordinate import Coordinate
from reciever import Reciever
from bullet import Bullet
# circurated reference
# import gameManager
class Unit(GameObject):
  def __init__(self, position, direction, gameManager, teamFlag, reciever):
    super().__init__(position = position, direction = direction)
    self._startingPoint = position
    self._startingDirection = direction
    self.initialize()
    self._idForAi = 0
    self._teamFlag = teamFlag
    self._reciever = reciever
    self._reciever.setPosition(position)
    self._reciever.setDirection(direction)
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
  def setHp(self,_hp):
    self._hp = self._hp
  def getHp(self):
    return self._hp
  def setAttackPower(self, _attackPower):
    self._attackPower = _attackPower
  def getAttackPower(self):
    return self._attackPower
  def sendData(self):
    #todo
    self._reciever.setPosition(self.getPosition())
    self._reciever.setDirection(self.getDirection())
  def recieveData(self):
    self.setPosition(self._reciever.getPosition())
    self.setDirection(self._reciever.getDirection())
    if self._term <= 0:
      if self._reciever.getFiring():
        self.makeBullet()
  def step(self):
    if self._term > 0:
      self._term -= 1
    self.sendData()
    self._reciever.step()
    self.recieveData()

    super().step()
    


