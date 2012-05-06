from . coordinate import Coordinate

_pushedKeys = set()
_mousePosition = Coordinate()

class KeyData:
    @staticmethod
    def setKeyStatus(keyId, value):
        if value:
            _pushedKeys.add(keyId)
        elif keyId in _pushedKeys:
            _pushedKeys.remove(keyId)
    @staticmethod
    def getKeyStatus(keyId):
        return keyId in _pushedKeys
    @staticmethod
    def setMousePosition(pos):
        global _mousePosition
        _mousePosition = Coordinate(pos)
    @staticmethod
    def getMousePosition():
        return _mousePosition
