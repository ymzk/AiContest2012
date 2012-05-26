from gameConfig import FIELD_CELL_HEIGHT, FIELD_CELL_WIDTH

def index(field, position):
  return (int(position[0] // FIELD_CELL_WIDTH), int(position[1] // FIELD_CELL_HEIGHT))
