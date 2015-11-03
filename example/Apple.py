class Apple(object):
 def _init_(self,nm="soft"):
  self.name=nm
  print("create a instanse")
 def showName(self):
  print("your name is",self.name)

apple=Apple()
apple._init_()
apple.showName()
apple1=Apple()
print apple==apple1