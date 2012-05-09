import sys
import time

while True:
  while sys.stdin.readline() == "end\n":
    print("start")
    print("fire")
    print("move 10")
    print("rotate 0.1")
    print("end")
    sys.stdout.flush()
  time.sleep(0.01)
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
