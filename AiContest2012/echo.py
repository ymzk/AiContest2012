from sys import stdin, stdout

with open('echo.log', 'w') as log:
  print('start echo', file = log)
  log.flush()
  while True:
    '''
    while True:
      print(sys.stdin.readline())
      sys.stdout.flush()
      '''
    while not stdin.closed:
      line = stdin.readline().strip()
      print(line)
      stdout.flush()
      print(line, file = log)
      log.flush()
    print ("endfile")
    log.flush()
    sys.stdout.flush()
