from aiInterface import AiInterface
from math import atan2
class AimAi(AiInterface):
  def send(self):
    self.log(len(self.units))
    for i in self.units:
      if i.team == self.myunit.team:
        continue
      else:
        angle = atan2(i.position[1] - self.myunit.position[1], i.position[0] - self.myunit.position[0])
        self.sendData(speed = 3, angle = self.regularizeAngle(angle - self.myunit.direction),fireing = True)
        self.log(self.regularizeAngle(angle - self.myunit.direction),self.myunit.direction)
        return
    self.sendData(fireing = True)
    return
if __name__ == "__main__":
  ai = AimAi()
  #ai.run(open("initMessage","r"),open("message","r"))
  ai.run()
