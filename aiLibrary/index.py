
def index(field, position):
  return (int(position[0] // field.cellwidth), int(position[1] // field.cellheight))
