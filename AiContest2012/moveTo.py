from aiInterface import AiInterface

class MoveTo(aiInterface):
  def moveTo(self):
    queue = []
    flagList = [[self.field.isPassable(w,h) for h in self.field.height]for w in self.field.width]
    def checkPoint(x, y, comeFrom):
      if 0 <= x < self.width and 0 <= y < self.height:
        if flagList[x][y] == True:
          flagList = comeFrom
    def addAround(x, y):
      queue.append((x+1, y, (-1, 0)))
      queue.append((x, y+1, (0, -1)))
      queue.append((x-1, y, (1, 0)))
      queue.append((x, y-1, (0, 1)))
    


