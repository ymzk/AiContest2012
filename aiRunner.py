import os
import sys
sys.path.append(os.path.abspath('ai'))
sys.path.append(os.path.abspath('aiLibrary'))
sys.path.append(os.path.abspath('setting'))
sys.path.append(os.path.abspath('graphics'))
sys.path.append(os.path.abspath('AiContest2012'))
sys.path.append(os.path.abspath('config'))
sys.path.append(os.path.abspath('mapData'))

os.chdir(os.path.abspath('ai'))

# exec("import " + sys.argv[1][:-3])
# __import__(sys.argv[1][:-3])
with open(sys.argv[1]) as source:
  exec(source.read())
