class Animal:
    def __init__(self, name, ext):
        self.name = name
        self.ext = ext
        print("父类构造函数")

    def eat(self, name):
        print("父类方法")

class Dog(Animal):
    def __init__(self, name, ext):
        super().__init__(name, ext)
        print("Dog构造函数", name)

    def eat(self, name):
        print("子类方法 ",name)


class Ext():
    def __init__(self, s):
        self.s = s
    def a(self):
        print("扩展",self.s)

class Groupss():
    def __init__(self):
        self.list = []
        print("组实例化")
    def add(self, s):
        self.list.append(s)
s = Groupss()
s.add(Ext("df"))
s.add(Ext("qqqq"))

dao = Dog('s', s)
dao.eat('23232')
for temp in dao.ext.list:
    temp.a()
print("duixiang ",dao.name)