from aiInterface import AiInterface

class TestAi(AiInterface):
  def send(self):
    self.sendData(speed = 3, angle = 0.2, fireing = True)

if __name__ == "__main__":
  testAi = TestAi()
  #testAi.run(open("initMessage","r"),open("message","r"))
  testAi.run()

