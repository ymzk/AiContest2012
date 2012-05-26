# coding: cp932
from gameConfig import FIELD_CELL_WIDTH, FIELD_CELL_HEIGHT

def getProcess2(source, destination):
  '''
    sourceからdestinationへ移動する時に通る座標のリストを返す関数。
    返る座標のリストはFieldのインデックスになっている。
  '''
  source = (int(source[0]), int(source[1]))
  destination = (int(destination[0]), int(destination[1]))
  diff = (destination[0] - source[0], destination[1] - source[1])
  if diff[0] == 0 and diff[1] == 0:
    yield (source[0] // FIELD_CELL_WIDTH, source[1] // FIELD_CELL_HEIGHT)
    return
  if diff[0] == 0:
    dy = diff[1] // abs(diff[1])
    for i in range(source[1] // FIELD_CELL_HEIGHT, destination[1] // FIELD_CELL_HEIGHT + dy, dy):
      yield (source[0] // FIELD_CELL_WIDTH, i)
    return
  if diff[1] == 0:
    dx = diff[0] // abs(diff[0])
    for i in range(source[0] // FIELD_CELL_WIDTH, destination[0] // FIELD_CELL_WIDTH + dx, dx):
      yield (i, source[1] // FIELD_CELL_HEIGHT)
    return
  dx = diff[0] // abs(diff[0])
  dy = diff[1] // abs(diff[1])
  lasty = source[1] // FIELD_CELL_HEIGHT
  if diff[0] > 0:
    for x in range(source[0] // FIELD_CELL_WIDTH, destination[0] // FIELD_CELL_WIDTH, dx):
      for y in range(lasty, (source[1] + ((diff[1] * abs((x + dx) * FIELD_CELL_WIDTH - source[0])) // abs(diff[0]))) // FIELD_CELL_HEIGHT + dy, dy):
        yield (x, y)
      lasty = (source[1] + diff[1] * abs((x + dx) * FIELD_CELL_WIDTH - source[0]) // abs(diff[0])) // FIELD_CELL_HEIGHT
    for y in range(lasty, destination[1] // FIELD_CELL_HEIGHT + dy, dy):
      yield (destination[0] // FIELD_CELL_WIDTH, y)
  else:
    for x in range(source[0] // FIELD_CELL_WIDTH, destination[0] // FIELD_CELL_WIDTH, dx):
      for y in range(lasty, (source[1] + ((diff[1] * abs(x * FIELD_CELL_WIDTH - source[0])) // abs(diff[0]))) // FIELD_CELL_HEIGHT + dy, dy):
        yield (x, y)
      lasty = (source[1] + diff[1] * abs(x * FIELD_CELL_WIDTH - source[0]) // abs(diff[0])) // FIELD_CELL_HEIGHT
    for y in range(lasty, destination[1] // FIELD_CELL_HEIGHT + dy, dy):
      yield (destination[0] // FIELD_CELL_WIDTH, y)

if __name__ == '__main__':
  for p in getProcess2((9, 9), (42, 68)):
    print(p)
