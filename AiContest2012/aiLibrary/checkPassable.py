from . getProcess import getProcess

def checkPassable(field, source, destination):
    for position in getProcess(source, destination):
        if not field.isPassable(position[0], position[1]):
            return False
    return True
