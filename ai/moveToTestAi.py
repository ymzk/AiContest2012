from aiLibrary.moveTo import MoveTo
from aiInterface import AiInterface, Action
import sys
import time

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
#    self.count = 0
#    self.last = int(time.time()) + 1
#    self.log = Log('moveToTest')
  def main(self):
#    if time.time() > self.last:
#      print(self.count, file = sys.stderr)
#      self.count = 0
#      self.last = int(time.time()) + 1
#    self.count += 1
#    print(self.myunit.position, file = sys.stderr)
#    sys.stderr.flush()
    return self.moveTo(self.bases[self.getOpponentTeamId()].position)
#    if self.move == None:
#      self.move = MoveTo(self.field, self.myunit, self.bases[1 - self.myunit.team].position)
#    return Action(*self.move.get(self.field, self.myunit))

if __name__ == "__main__":
  ai = MoveToTestAi()
  #ai.run(open("initMessage","r"),open("message","r"))
  ai.run()

