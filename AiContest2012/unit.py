# from ymzkgame import *
from ymzkgame.gameObject import GameObject
from ymzkgame.coordinate import Coordinate
from reciever import Reciever
from bullet import Bullet
# circurated reference
# import gameManager
class Unit(GameObject):
  def __init__(self, position, direction, gameManager, teamFlag):
    super().__init__(position = position, direction = direction)
    self._startingPoint = position
    self._startingDirection = direction
    self.initialize()
    self._idForAi = 0
    self._teamFlag = teamFlag
    self._reciever = Reciever(self, position, direction)
    self._gameManager = gameManager
  def initialize(self):
    self.setPosition(self._startingPoint)
    self.setDirection(self._startingDirection)
    self._timeNextFireing = 1
    self._term = 0
    self._hp = 100
    self._attackPower = 10
  def makeBullet(self):
    bullets.append(Bullet(self));
    self_timeNextFireing = 10;
  def changeState(self):
    if self._hp <= 0 :
      #死んだときの処理
      self.initialize()
  def getTeamFlag(self):
    return self._teamFlag
  def damage(self, attackObject):
    if self.getTeamFlag() != attackObject.getTeamFlag():
      self._hp -= attackObject.getAttackPower()
      attackObject.end()
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
  def recieveData(self):
    self.setPosition(self._reciever.getPosition())
    self.setDirection(self._reciever.getDirection())
    if self._term <= 0:
      if self._reciever.getFiring():
        self._gameManager.addBullet(Bullet(self))
        self._term = self._timeNextFireing
  def step(self):
    if self._term > 0:
      self._term -= 1
    self.setPosition(self.getPosition() + Coordinate(10,10))
    '''
    self.sendData()
    self._reciever.step()
    self.recieveData()
    '''
    super().step()
    


