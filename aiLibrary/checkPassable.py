from . getProcess2 import getProcess2
import sys

def checkPassable(field, source, destination):
#    print('checkPassable(%s, %s)' % (str(source), str(destination)), file = sys.stderr)
    for position in getProcess2(source, destination):
#        print('cehckPassable:', position, field.fieldData[position[0]][position[1]], field.isPassable(position[0], position[1]), file = sys.stderr)
#        sys.stderr.flush()
        if not field.isPassable(position[0], position[1]):
#            print(position, 'is not passable', file = sys.stderr)
#            sys.stderr.flush()
            return False
#    sys.stderr.flush()
    return True
