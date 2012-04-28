from ymzkgame.runner import run
from ymzkgame.runnable import Runnable
from ymzkgame.gameObject import GameObject
from ymzkgame.moveClasses import *
from ymzkgame.manager import Manager
from ymzkgame.coordinate import Coordinate

class Test(Runnable):
    def __init__(self):
        self.obj = GameObject(position = (400, 300))
    def step(self):
        if Manager.getKeyStatus(Manager.K_UP):
            self.obj.setPosition(self.obj.getPosition() + Coordinate(0, -1))
        if Manager.getKeyStatus(Manager.K_LEFT):
            self.obj.setPosition(self.obj.getPosition() + Coordinate(-1, 0))
        if Manager.getKeyStatus(Manager.K_DOWN):
            self.obj.setPosition(self.obj.getPosition() + Coordinate(0, 1))
        if Manager.getKeyStatus(Manager.K_RIGHT):
            self.obj.setPosition(self.obj.getPosition() + Coordinate(1, 0))
        self.obj.step()

run(Test())
