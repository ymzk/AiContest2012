hoge = open("map.data","w")

Field = [["NO" for i in range(40)] for j in range(40)]
Field[20][0] = "B0"
#base
for i in range(10):
  for j in range(10):
    Field[i][j] = "O0"
    #ownaria
for i in range(10,30):
  Field[i][19] = "WA"
  #wall
for i in range(len(Field)):
  for j in range(len(Field[i])):
    hoge.write(Field[j][i]+" ")
  hoge.write("\n")
hoge.close()
