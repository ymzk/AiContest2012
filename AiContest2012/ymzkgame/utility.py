from coordinate import Coordinate

class Iterator:
    def __iter__(self):
        return self
    def __next__(self):
        return NotImplemented

def toTuple(obj):
    if isinstance(obj, Coordinate):
        return (obj.x, obj.y)
    else:
        return tuple(obj)
