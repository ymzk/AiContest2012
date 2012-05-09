
hoge = open("map.data","w")
Field = [["0" for i in range(20)] for j in range(40)]
Field[20][0] = "2"
#base
for i in range(10):
  for j in range(10):
    Field[i][j] = "3"
    #ownaria
for i in range(10,30):
  Field[i][19] = "1"
  #wall
for i in range(20):
  for j in range(40):
    hoge.write(Field[j][i]+" ")
  hoge.write("\n")
hoge.close()
