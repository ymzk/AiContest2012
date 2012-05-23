# coding: cp932
from aiLibrary.aiInterface import AiInterface
from math import atan2
class AimAi(AiInterface):
  def main(self):
    self.log(len(self.units))
    for i in self.units:
      if i.team == self.myunit.team:
        continue
      else:
        angle = atan2(i.position[1] - self.myunit.position[1], i.position[0] - self.myunit.position[0])
        result = Action(speed = 3, rollAngle = self.regularizeAngle(angle - self.myunit.direction),firing = True)
        self.log(self.regularizeAngle(result)
        return result
#    self.sendData(firing = True)
    return Action(speed = 0, rollAngle = 0, firing = True)
  '''
    古い仕様　現在この仕様は利用できません
  def send(self):
    self.log(len(self.units))
    for i in self.units:
      if i.team == self.myunit.team:
        continue
      else:
        angle = atan2(i.position[1] - self.myunit.position[1], i.position[0] - self.myunit.position[0])
        self.sendData(speed = 3, angle = self.regularizeAngle(angle - self.myunit.direction),firing = True)
        self.log(self.regularizeAngle(angle - self.myunit.direction),self.myunit.direction)
        return
    self.sendData(firing = True)
    return
  '''
ai = AimAi()
#ai.run(open("initMessage","r"),open("message","r"))
ai.run()
