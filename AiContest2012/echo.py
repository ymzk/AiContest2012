import sys


while True:
  '''
  while True:
    print(sys.stdin.readline())
    sys.stdout.flush()
    '''
  for i in sys.stdin:
    print (i)
    sys.stdout.flush()
  print ("endfile")
