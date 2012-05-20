import os
import sys
sys.path.append(os.path.abspath('AiContest2012'))
os.chdir('AiContest2012')

import gameManager
from ymzkgame import runner

if __name__ == '__main__':
  runner.run(gameManager.GameManager())
