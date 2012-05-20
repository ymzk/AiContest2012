from . coordinate import Coordinate
from . move import Move

DEFAULT_TITLE = 'no title'

DEFAULT_IMAGE = 'default.bmp'
DEFAULT_PERMEATE = True

DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
DEFAULT_SCREEN_SIZE = (DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)

DEFAULT_FPS = 60

DEFAULT_IMAGE = 'ymzkgame/default.bmp'
DEFAULT_POSITION = Coordinate(0, 0)
DEFAULT_DIRECTION = 0

class NoMove(Move):
    def __call__(self, position, direction):
        return self, position, direction

DEFAULT_MOVE = NoMove()
