from ymzkgame.runner import run
from ymzkgame.runnable import Runnable
from ymzkgame.gameObject import GameObject
from ymzkgame.moveClasses import *
from ymzkgame.manager import Manager
from ymzkgame.coordinate import Coordinate
from ymzkgame.image import Image

run(GameObject(image = Image().getSubImage((16, 16), (16, 16)), move = MoveByKey(velocity = 2)))
