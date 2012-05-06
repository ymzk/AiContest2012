from ymzkgame.runner import run
from ymzkgame.runnable import Runnable
from ymzkgame.gameObject import GameObject
from ymzkgame.moveClasses import *
from ymzkgame.manager import Manager
from ymzkgame.coordinate import Coordinate

run(GameObject(move = MoveByKey(velocity = 2)))
