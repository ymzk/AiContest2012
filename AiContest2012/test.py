class hogec:
  def name(self):
    print(self.__module__)

class fooc(hogec):
  pass
hoge = fooc()
hoge.name()
