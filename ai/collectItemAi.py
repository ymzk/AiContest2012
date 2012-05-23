# coding: cp932
from aiLibrary.aiInterface import AiInterface, Action
from aiLibrary.moveTo import MoveTo
from math import atan2
class CollectItemAi(AiInterface):
  def initCalculation(self):
    self.log('\n'.join(str(i) for i in self.field.fieldData))
    self.baseMove = None
    for w in range(self.field.width):
      for h in range(self.field.height):
        if self.field.fieldData[w][h] == -1:
          self.itemMove = MoveTo(self.field, self.myunit, ((w + 0.5) * self.field.cellWidth, (h + 0.5) * self.field.cellHeight))
          self.log(self.itemMove.path)
          return
  def main(self):
    if self.myunit.attack <= 10:
      for i in self.units:
        if i.team == self.myunit.team:
          continue
        else:
          angle = atan2(i.position[1] - self.myunit.position[1], i.position[0] - self.myunit.position[0])
          return Action(speed = 3, rollAngle = self.regularizeAngle(angle - self.myunit.direction),firing = True)
      return Action(*self.itemMove.get(self.field, self.myunit))
    for opponent in self.bases:
      if opponent.team == self.myunit.team:
        continue
      if (self.myunit.position[0] - opponent.position[0]) ** 2 + (self.myunit.position[1] - opponent.position[1]) ** 2 < 360000:
        if self.canShoot(self.myunit.position, opponent.position):
          return Action(3,self.regularizeAngle(atan2(opponent.position[1] - self.myunit.position[1], opponent.position[0] - self.myunit.position[0]) - self.myunit.direction),firing = True)
    for i in self.units:
      if i.team == self.myunit.team:
        continue
      else:
        angle = atan2(i.position[1] - self.myunit.position[1], i.position[0] - self.myunit.position[0])
        return Action(speed = 3, rollAngle = self.regularizeAngle(angle - self.myunit.direction),firing = True)
    if self.baseMove == None:
      self.baseMove = MoveTo(self.field, self.myunit, self.bases[1 - self.myunit.team].position)
    return Action(*self.baseMove.get(self.field, self.myunit))
  '''
    古い仕様　現在この仕様は利用できません
  def send(self):
    if self.myunit.attack <= 10:
      for i in self.units:
        if i.team == self.myunit.team:
          continue
        else:
          angle = atan2(i.position[1] - self.myunit.position[1], i.position[0] - self.myunit.position[0])
          self.sendData(speed = 3, angle = self.regularizeAngle(angle - self.myunit.direction),firing = True)
          return
      self.sendData(*self.itemMove.get(self.field, self.myunit))
      return
    for opponent in self.bases:
      if opponent.team == self.myunit.team:
        continue
      if (self.myunit.position[0] - opponent.position[0]) ** 2 + (self.myunit.position[1] - opponent.position[1]) ** 2 < 360000:
        if self.canShoot(self.myunit.position, opponent.position):
          self.sendData(3,self.regularizeAngle(atan2(opponent.position[1] - self.myunit.position[1], opponent.position[0] - self.myunit.position[0]) - self.myunit.direction),firing = True)
          return
    for i in self.units:
      if i.team == self.myunit.team:
        continue
      else:
        angle = atan2(i.position[1] - self.myunit.position[1], i.position[0] - self.myunit.position[0])
        self.sendData(speed = 3, angle = self.regularizeAngle(angle - self.myunit.direction),firing = True)
        return
    if self.baseMove == None:
      self.baseMove = MoveTo(self.field, self.myunit, self.bases[1 - self.myunit.team].position)
    self.sendData(*self.baseMove.get(self.field, self.myunit))
    return
    '''

ai = CollectItemAi()
#ai.run(open("initMessage","r"),open("message","r"))
ai.run()
