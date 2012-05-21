
def index(field, position):
  return (int(position[0] // field.cellWidth), int(position[1] // field.cellHeight))
