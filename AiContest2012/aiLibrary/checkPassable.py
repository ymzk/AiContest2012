from . getProcess import getProcess

def checkPassable(field, source, destination):
    for position in getProcess(source, destination):
        if not field.isPassable(position[1], position[0]):
            return False
    return True
