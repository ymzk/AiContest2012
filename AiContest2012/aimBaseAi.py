from aiInterface import AiInterface
from aiLibrary.moveTo import MoveTo
from math import atan2
class AimBaseAi(AiInterface):
  def initCalculation(self):
    self.move = None
  def send(self):
    opponent = self.bases[1 - self.myunit.team]
    if (self.myunit.position[0] - opponent.position[0]) ** 2 + (self.myunit.position[1] - opponent.position[1]) ** 2 < 360000:
      if self.canShoot(self.myunit.position, opponent.position):
        self.sendData(0,self.regularizeAngle(atan2(opponent.position[1] - self.myunit.position[1], opponent.position[0] - self.myunit.position[0]) - self.myunit.direction),firing = True)
        return
    if self.move == None:
      self.move = MoveTo(self.field, self.myunit, self.bases[1 - self.myunit.team].position)
    self.sendData(*self.move.get(self.field, self.myunit))
    return


if __name__ == "__main__":
  ai = AimBaseAi()
  #ai.run(open("initMessage","r"),open("message","r"))
  ai.run()
