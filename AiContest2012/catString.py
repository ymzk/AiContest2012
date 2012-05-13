
class CatString:
  def __init__(self, buffer = ''):
    self._buffer = buffer
  def write(self, value):
    if len(self._buffer) != 0:
      self._buffer += ' '
    self._buffer += str(value)
  def getString(self):
    return self._buffer
  def str(self):
    return self.getString()
  def __str__(self):
    return self.getString()
