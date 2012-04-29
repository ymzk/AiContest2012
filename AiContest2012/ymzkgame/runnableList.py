from ymzkgame.runnable import Runnable

class RunnableList(list, Runnable):
    def __init__(self, *args):
        if len(args) == 0:
            list.__init__(self)
            Runnable.__init__(self)
        elif len(args) == 1:
            list.__init__(self, args[0])
            Runnable.__init__(self)
        else:
            list.__init__(self, args)
            Runnable.__init__(self)
    def step(self):
        i = 0
        while i < len(self):
            if not self[i].isValid():
                del self[i]
            else:
                i += 1
        for i in self:
            i.step()
