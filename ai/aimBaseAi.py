# coding: cp932
import sys
import os
print(sys.path)
from aiLibrary.moveTo import MoveTo
from aiLibrary.aiInterface import AiInterface, Action
from math import atan2
class AimBaseAi(AiInterface):
  def initCalculation(self):
    # self.move = None
    pass
  def main(self):
    for i in self.units:
      if i.team == self.myunit.team:
        continue
      else:
        if self.canShoot(self.myunit.position, i.position):
          angle = atan2(i.position[1] - self.myunit.position[1], i.position[0] - self.myunit.position[0])
          return Action(speed = 3, rollAngle = self.regularizeAngle(angle - self.myunit.direction),firing = True)
    try:
      opponentBase = self.bases[self.getOpponentTeamId()]
    except (IndexError, AttributeError):
      return Action()
    if (self.myunit.position[0] - opponentBase.position[0]) ** 2 + (self.myunit.position[1] - opponentBase.position[1]) ** 2 < 360000:
      if self.canShoot(self.myunit.position, opponentBase.position):
        return Action(0,self.regularizeAngle(atan2(opponentBase.position[1] - self.myunit.position[1], opponentBase.position[0] - self.myunit.position[0]) - self.myunit.direction),firing = True)
    # if self.move == None:
    #   self.move = MoveTo(self.field, self.myunit, self.bases[self.getOpponentTeamId()].position)
    return self.moveTo(self.bases[self.getOpponentTeamId()].position)
  '''
    古い仕様　現在この仕様は利用できません
  def send(self):
    for i in self.units:
      if i.team == self.myunit.team:
        continue
      else:
        if self.canShoot(self.myunit.position, i.position):
          angle = atan2(i.position[1] - self.myunit.position[1], i.position[0] - self.myunit.position[0])
          self.sendData(speed = 3, angle = self.regularizeAngle(angle - self.myunit.direction),firing = True)
          return
    for opponent in self.bases:
      if opponent.team == self.myunit.team:
        continue
      if (self.myunit.position[0] - opponent.position[0]) ** 2 + (self.myunit.position[1] - opponent.position[1]) ** 2 < 360000:
        if self.canShoot(self.myunit.position, opponent.position):
          self.sendData(0,self.regularizeAngle(atan2(opponent.position[1] - self.myunit.position[1], opponent.position[0] - self.myunit.position[0]) - self.myunit.direction),firing = True)
          return
    if self.move == None:
      self.move = MoveTo(self.field, self.myunit, self.bases[1 - self.myunit.team].position)
    self.sendData(*self.move.get(self.field, self.myunit))
    return
  '''

if __name__ == "__main__":
  ai = AimBaseAi()
  #ai.run(open("initMessage","r"),open("message","r"))
  ai.run()
