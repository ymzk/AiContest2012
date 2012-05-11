class MakeField:
  def __init__(self, filename = "map.data"):
    self._file = open(filename, "w")
  def makeField(self, width, height):
    self._field = [["NO" for i in range(height)] for j in range(width)]
  def writeRect(self, code, lupoint, rdpoint):
    for i in range(lupoint[0],rdpoint[0]):
      for j in range(lupoint[1],rdpoint[1]):
        self.write(code, (i, j))
  def write(self, code, point):
    if 0 <= point[0] < len(self._field[0]):
      if 0 <= point[1] < len(self._field):
        self._field[point[0]][point[1]] = code
  def output(self):
    for i in range(len(Field)):
      for j in range(len(Field[i])):
        self._file.write(Field[j][i]+" ")
      self._file.write("\n")
    self._file.close()

hoge = MakeField()
hoge.makeField(41,41)
  
