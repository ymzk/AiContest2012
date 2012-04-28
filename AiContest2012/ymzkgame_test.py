from ymzkgame.runner import run
from ymzkgame.runnable import Runnable
from ymzkgame.gameObject import GameObject
from ymzkgame.moveClasses import *
from ymzkgame.manager import Manager
from ymzkgame.coordinate import Coordinate
from math import sin, cos
from math import pi as PI
from ymzkgame.runnableList import RunnableList

class BG(Runnable):
    def step(self):
        Manager.getScreen().fill((200, 200, 200))

class Test(Runnable):
    def __init__(self, pos):
        self.v = 1
        self.vv = 0.1
#        self.obj = GameObject(image = 'ymzkgame/test.bmp', position = (400, 300))
        self.obj = GameObject(position = pos)
    def step(self):
        '''
        if Manager.getKeyStatus(Manager.K_UP):
            d = Coordinate(*(f(self.obj.getDirection() - PI / 2) for f in (cos, sin)))
            self.obj.setPosition(self.obj.getPosition() + self.v * d)
        if Manager.getKeyStatus(Manager.K_LEFT):
            self.obj.setDirection(self.obj.getDirection() + self.vv)
        if Manager.getKeyStatus(Manager.K_RIGHT):
            self.obj.setDirection(self.obj.getDirection() - self.vv)
        '''
        if Manager.getKeyStatus(Manager.K_UP):
            self.obj.setPosition(self.obj.getPosition() + Coordinate(0, -self.v))
        if Manager.getKeyStatus(Manager.K_LEFT):
            self.obj.setPosition(self.obj.getPosition() + Coordinate(-self.v, 0))
        if Manager.getKeyStatus(Manager.K_DOWN):
            self.obj.setPosition(self.obj.getPosition() + Coordinate(0, self.v))
        if Manager.getKeyStatus(Manager.K_RIGHT):
            self.obj.setPosition(self.obj.getPosition() + Coordinate(self.v, 0))
        self.obj.step()

run(RunnableList(BG(), Test((400, 300)), Test((0, 0))))
