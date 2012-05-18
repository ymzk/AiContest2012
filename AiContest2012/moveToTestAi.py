from aiLibrary.moveTo import MoveTo
from aiInterface import AiInterface
import sys

INF = float('inf')
'''
class Log:
  def __init__(self, filename):
    if filename[-4:] != '.log':
      filename += '.log'
    self.file = open(filename, 'w')
  def close(self):
    self.file.close()
  def __del__(self):
    self.close()
  def log(self, *args, **kwds):
    print(*args, file = self.file, **kwds)
    self.file.flush()
  def write(self, *args):
    self.file.write(*args)
    self.file.flush()
  def __enter__(self):
    pass
  def __exit__(self, *args):
    self.close()
'''
class MoveToTestAi(AiInterface):
  def __init__(self):
    AiInterface.__init__(self)
    self.move = None
#    self.log = Log('moveToTest')
  def send(self):
    print(self.myunit.position, file = sys.stderr)
    sys.stderr.flush()
#    print('start MoveToTestAi.send', file = self.log)
    if self.move == None:
#      self.log.log('start initialize move')
      self.move = MoveTo(self.field, self.myunit, self.bases[1 - self.myunit.team].position)
#      self.log.log('sccess initialize move')
    self.sendData(*self.move.get(self.field, self.myunit))
#      self.sendData(speed = INF, angle = 0, fire = False)

if __name__ == "__main__":
  ai = MoveToTestAi()
  #ai.run(open("initMessage","r"),open("message","r"))
  ai.run()

