import sys
import time

logfile = open("hoge.log","w")
def log(*messages):
  print(*messages, file = logfile)
  logfile.flush()

log("start")
while True:
  message = sys.stdin.readline().split()
  log('Meesage:', message)
  flag = True
  if 'end' in message:
    print("10 0.1 1")
  else:
    print("0 0 0")
  sys.stdout.flush()
  time.sleep(0.01)
log('end')
logfile.close()
'''
while True:
  
  while True:
    print(sys.stdin.readline())
    sys.stdout.flush()
  for i in sys.stdin:
    print (i)
    sys.stdout.flush()
  print ("endfile")
  
  '''
