import sys
import time

logfile = open("hoge.log","w")
def log(*messages):
  print(*messages, file = logfile)
  logfile.flush()

log("start")
while True:
  message = sys.stdin.readline().strip()
  log('Meesage:', message)
  if message == 'end':
    log('action')
    print("start")
    print("fire")
    print("move 10")
    print("rotate 0.1")
    print("end")
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
