from subprocess import Popen, PIPE
import re
import sys
from time import time, sleep
from queue import Full, Empty
from threading import Thread, Event
from mythreading.synchronized_queue import SynchronizedQueue

def processControllerCore(command, sendQueue, recvQueue, invalid):
  subprocess = Popen(command,
                     shell = False,
                     stdin = PIPE,
                     stdout = PIPE,
                     stderr = None)
  try:
    while not invalid.isSet():
      while sendQueue.empty():
        sleep(0.01)
      while not sendQueue.empty():
        flag, sendMessage = sendQueue.pop()
      print('sendMessage: ' + str(sendMessage) + '\n', end = '')
      subprocess.stdin.write(sendMessage.encode())
      subprocess.stdin.write(b'\n')
      subprocess.stdin.flush()
      recvMessage = subprocess.stdout.readline().decode().strip()
      recvQueue.push(recvMessage)
  finally:
    subprocess.kill()

class ProcessController():
  def __init__(self, executableName):
    if executableName[-3:] == '.py':
      command = ["C:\\Python32\\python.exe",executableName]
    elif executableName[-4:] == '.exe':
      command = ["./" + executableName]
    else:
      raise RuntimeError('ProcessController can\'t run this program')
    sendQueue, recvQueue = SynchronizedQueue(3), SynchronizedQueue()
    terminate = Event()
    t = Thread(target = processControllerCore, args = (command, sendQueue, recvQueue, terminate))
    t.start()
    self._terminate = terminate
    self._childThread = t
    self._sendQueue = sendQueue
    self._recvQueue = recvQueue
  def write(self, message):
    if self._sendQueue.full():
      self._sendQueue.noWaitPop()
    self._sendQueue.noWaitPush(message)
  def flush(self):
    pass
  def __iter__(self):
    return self
  def __next__(self):
    return self.readline()
  def readline(self):
    flag, result = self._recvQueue.pop()
    if not flag:
      return None
    else:
      return result
  def close(self):
    pass
  def end(self):
    self._terminate.set()

  
if __name__ == "__main__":
  def f(terminater):
    counter = 0
    while not terminater.isSet():
      counter += 1
#    print(counter)
  terminater = Event()
  ts = [Thread(target = f, args = (terminater,)) for i in range(20)]
  [t.start() for t in ts]
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
    print(msg)
  pc.end()
  terminater.set()
  '''
  pc.write("end\n".encode())
  pc.flush()
  print("wrote end")
  sys.stdout.flush()
#  pc.p.stdin.write(b"hoge\n")
#  pc.p.stdin.flush()
  for j in pc:
    print("stdout = ", j.decode())
    sys.stdout.flush()
    if j == b"\n":
      print("only return")
      sys.stdout.flush()
      continue
    print("write foo")
    pc.write("foo\n".encode())
    pc.flush()
    sys.stdout.flush()
  print("end pc\n")
  sys.stdout.flush()
    '''
