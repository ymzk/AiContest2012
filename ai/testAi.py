#coding: cp932
from aiLibrary.aiInterface import AiInterface

class TestAi(AiInterface):
  def main(self):
    return Action(speed = 3, rollAngle = 0.2, firing = True)
  '''
    古い仕様　現在この仕様は利用できません
  def send(self):
    self.sendData(speed = 3, angle = 0.2, firing = True)
  '''

testAi = TestAi()
#testAi.run(open("initMessage","r"),open("message","r"))
testAi.run()

