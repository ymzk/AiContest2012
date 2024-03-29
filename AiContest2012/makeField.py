class MakeField:
  def __init__(self, file = open("map.data", "w")):
    self._file = file
    self._unitposition = [[],[]]
  def unitposition(self,point,team):
    self._unitposition[team].append(point)
  def makeField(self, width, height):
    self._field = [["NO" for i in range(height)] for j in range(width)]
  def writeRect(self, code, lupoint, rdpoint):
    for i in range(lupoint[0],rdpoint[0] + 1):
      for j in range(lupoint[1],rdpoint[1] + 1):
        self.write(code, (i, j))
  def writeLineRect(self, code, lupoint, rdpoint):
    for i in range(lupoint[0],rdpoint[0]+1):
      self.write(code,(i,lupoint[1]))
      self.write(code,(i,rdpoint[1]))
    for j in range(lupoint[1],rdpoint[1]+1):
      self.write(code, (lupoint[0], j))
      self.write(code, (rdpoint[0], j))
  def write(self, code, point):
    if 0 <= point[0] < len(self._field[0]):
      if 0 <= point[1] < len(self._field):
        self._field[point[0]][point[1]] = code
  def output(self):
    print(len(self._field[0]),len(self._field),file = self._file)
    for l in self._unitposition:
      for i in l:
        print(i,end = " ",file = self._file)
      print(file = self._file)
    for i in range(len(self._field)):
      for j in range(len(self._field[i])):
        self._file.write(self._field[j][i]+" ")
      self._file.write("\n")
    self._file.close()
import sys
hoge = MakeField()
hoge.makeField(43,43)
hoge.write("B0",(21,6))
hoge.write("B1",(21,36))
hoge.writeRect("WA",(16,10),(26,10))
hoge.writeRect("WA",(16,32),(26,32))
hoge.writeRect("WA",(16,5),(26,5))
hoge.writeRect("WA",(16,37),(26,37))
hoge.write("IH",(1,1))
hoge.write("IH",(1,41))
hoge.write("IH",(41,1))
hoge.write("IH",(41,41))
hoge.write("IA",(21,21))
hoge.write("IA",(1,21))
hoge.write("IA",(41,21))
hoge.writeRect("O0",(11,1),(31,4))
hoge.writeRect("O1",(11,38),(31,42))
hoge.writeLineRect("WA",(0,0),(42,42))
hoge.unitposition((16,3,1.5),0)
hoge.unitposition((26,3,1.5),0)
hoge.unitposition((21,3,1.5),0)
hoge.unitposition((16,39,-1.5),1)
hoge.unitposition((26,39,-1.5),1)
hoge.unitposition((21,39,-1.5),1)
hoge.output()

