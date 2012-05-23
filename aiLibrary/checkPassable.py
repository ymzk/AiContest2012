from . getProcess import getProcess

def checkPassable(field, source, destination):
    for position in getProcess(source, destination):
#        import sys
#        print('cehckPassable:', position, field.fieldData[position[0]][position[1]], field.isPassable(position[0], position[1]), file = sys.stderr)
        if not field.isPassable(position[0], position[1]):
            return False
    return True
