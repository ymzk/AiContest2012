from subprocess import Popen, PIPE
import re
import sys
from time import time, sleep
from queue import Full, Empty
from threading import Thread, Event
from mythreading.synchronized_queue import SynchronizedQueue

'''
class ProcessControllerCore(Thread):
  def __init__(self, command, commandQueue, resultQueue):
    self.subprocess = Popen(command,
                            stdin = PIPE,
                            stdout = PIPE,
                            open('processControllerCoreChild.log', 'w'))
    self.commandQueue = commandQueue
    self.resultQueue = resultQueue
  def run(self):
    while True:
      while commandQueue.empty():
        sleep(0.001)
      cmd = commandQueue.pop()
      if cmd[0] == 'send':
        subprocess.stdin.write(cmd[1])
      elif cmd[0] == 'recieve':
        resultQueue.push(subprocess.stdout.readline())
      elif cmd[0] == 'kill':
        subprocess.kill()
        return
'''
def processControllerCore(subprocess, sendQueue, recvQueue):
#  try:
    while True:
      while sendQueue.empty():
        sleep(0.001)
      while not sendQueue.empty():
        flag, sendMessage = sendQueue.pop()
      print('sendMessage: ' + str(sendMessage) + '\n', end = '')
      subprocess.stdin.write(str(sendMessage).encode())
      # subprocess.stdin.write(str('end').encode())
      subprocess.stdin.write(b'\n')
      subprocess.stdin.flush()
      recvMessage = subprocess.stdout.readline().decode().strip()
      print('recvMessage: ' + str(recvMessage) + '\n', end = '')
      recvQueue.push(recvMessage)
#  except:
#    pass

#def sender(stdin, sendQueue):

class ProcessController():
  def __init__(self, executableName):
    if executableName[-3:] == '.py':
      command = ["C:\\Python32\\python.exe",executableName]
    elif executableName[-4:] == '.exe':
      command = ["./" + executableName]
    else:
      raise RuntimeError("ProcessController can\'t run this program " + executableName)
    print(command)
    self._childError = open('processControllerChild.log', 'w')
    subprocess = Popen(command,
                       stdin = PIPE,
                       stdout = PIPE,
                       stderr = self._childError)
    sendQueue, recvQueue = SynchronizedQueue(3), SynchronizedQueue()
    t = Thread(target = processControllerCore, args = (subprocess, sendQueue, recvQueue))
    t.start()
    self._childThread = t
    self._sendQueue = sendQueue
    self._recvQueue = recvQueue
    self._subprocess = subprocess
  def valid(self):
    return self._subprocess.poll() == None
  def __bool__(self):
    return self.valid()
  def write(self, message):
    if self._sendQueue.full():
      self._sendQueue.noWaitPop()
    self._sendQueue.noWaitPush(message)
  def flush(self):
    pass
  def __iter__(self):
    return self
  def __next__(self):
    if not self.valid():
      raise StopIteration()
    return self.readline()
  def readline(self):
    print('ProcessController.readline()\n', end = '')
    flag, result = self._recvQueue.pop()
    if not flag:
      return None
    else:
      print('pop: ' + str(result) + '\n', end = '')
      return result
  def close(self):
    pass
  def end(self):
    if self._subprocess.poll() == None:
      self._subprocess.kill()
    self._childError.close()
  
if __name__ == "__main__":
  '''
  def f(terminater):
    counter = 0
    while not terminater.isSet():
      counter += 1
#    print(counter)
  terminater = Event()
#  ts = [Thread(target = f, args = (terminater,)) for i in range(20)]
#  [t.start() for t in ts]
  pc = ProcessController("echo.py")
  sleep(3)
  for i in range(10):
    pc.write('hoge' + str(i))
    sleep(0.01)
    tmp = pc.readline()
    print(tmp)
  while True:
    msg = pc.readline()
    if msg == None:
      break
    print(str(msg) + '\n', end = '')
  pc.end()
  terminater.set()
  '''
  pc = ProcessController('hoge.py')
  pc.write("end")
  pc.flush()
  print("wrote end")
  sys.stdout.flush()
#  pc.p.stdin.write(b"hoge\n")
#  pc.p.stdin.flush()
  try:
    for j in pc:
      print("stdout = ", j)
      sys.stdout.flush()
      if j == b"\n":
        print("only return")
        sys.stdout.flush()
        continue
      print("write foo")
      sys.stdout.flush()
      pc.write("foo")
      pc.flush()
  finally:
    pc.end()
    print("end pc\n")
    sys.stdout.flush()
#  '''
