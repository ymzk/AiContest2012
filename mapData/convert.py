import pygame
import sys
args = sys.argv
import os

def isWall(r, g, b):
  return r + g + b < 200

def isBase(r, g, b):
  return g < 200 and 200 <= r + g + b < 400

def isOwnArea(r, g, b):
  return g < 200 and 400 <= r + g + b < 600

def isItem(r, g, b):
  return 200 <= r + g + b < 600 and g >= 200

def isNoneCell(r, g, b):
  return 600 <= r + g + b

def getTeamId(r, g, b):
  return '1' if b < r else '0'

def getItemType(r, g, b):
  return 'A' if b < r else 'H'

def convert(color):
#  print(color)
  color = color[:3]
  if isWall(*color):
    return 'WA'
  elif isBase(*color):
    return 'B' + getTeamId(*color)
  elif isOwnArea(*color):
    return 'O' + getTeamId(*color)
  elif isItem(*color):
    return 'I' + getItemType(*color)
  elif isNoneCell(*color):
    return 'NO'
  else:
    raise ValueError('can\'t convert: ' + str(color))

def main(imagefilename, out = sys.stdout):
  image = pygame.image.load(imagefilename)
  print(' '.join(str(i) for i in image.get_size()), file = out)
  for i in range(image.get_height()):
    print(
      ' '.join(convert(image.get_at((j, i))) for j in range(image.get_width())),
      file = out)

def usage():
  return 'usage: python convert.py imagefilename [outputfilename]'

if __name__ == '__main__':
  if len(args) == 1:
#    print(usage())
    main('testMap.bmp')
  elif len(args) == 2:
    main(args[1])
  elif len(args) == 3:
    with open(args[2], 'w') as out:
      main(args[1], out = out)
  else:
    print(usage())
