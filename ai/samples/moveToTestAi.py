from aiLibrary.moveTo import MoveTo
from aiLibrary.aiInterface import AiInterface, Action
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
#    self.move = None
#    self.count = 0
#    self.last = int(time.time()) + 1
#    self.log = Log('moveToTest')
    self.target = None
  def main(self):
#    print('\n'.join(str(i) for i in self.field.fieldstringdata), file = sys.stderr)
#    print('\n'.join(str(i) for i in self.field.fieldData), file = sys.stderr)
#    if time.time() > self.last:
#      self.log(self.count, file = sys.stderr)
#      self.count = 0
#      self.last = int(time.time()) + 1
#    self.count += 1
#    print(self.myunit.position, file = sys.stderr)
#    sys.stderr.flush()
    if self.target == None:
      for base in self.bases:
        if base.team == self.getAllyTeamId():
          continue
        self.target = base.position
        break
    return self.moveTo(self.target)
#    if self.move == None:
#      self.move = MoveTo(self.field, self.myunit, self.bases[1 - self.myunit.team].position)
#    return Action(*self.move.get(self.field, self.myunit))

ai = MoveToTestAi()
#ai.run(open("initMessage","r"),open("message","r"))
ai.run()

