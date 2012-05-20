from ymzkgame.image import Image
from ymzkgame.manager import Manager

def draw(screen, image, position, direction, viewPosition, viewDirection):
  PI = 3.14159265
  viewDirection += PI / 2
  image = Image(image)
  image = image.rotate(viewDirection - direction)
  screen.draw(image = image,
              position = (position -
                          viewPosition
                          ).rotate(-viewDirection) -
                          image.getSize() / 2 +
                          Manager.getScreenSize() / 2)
