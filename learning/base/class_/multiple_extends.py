'''
    多重继承，相比于单继承，区别貌似不大，反正这是一个动态性语言，所以类型的约束就没有那么明显
'''

class A:
    name = "A"
    __num = 1

    def __init__(self):
        print('A init')
        self.inita = 'init a'

    def show(self):
        print(self.name)
        print(self.__num)
    def set_num(self, num):
        self.__num = num


class B:
    nameb = "B"
    __numb = 2

    def __init__(self):
        print("b init")
        self.initb = 'init b'

    def show(self):
        print(self.nameb)
        print(self.__numb)
    def set_name(self, name):
        self.nameb = name

class C(A, B):

    def __init__(self):
        # 多重继承，就要多重的引用父类的构造器，通过构造器来得到父类的属性
        A.__init__(self)
        B.__init__(self)
        print('c init')
        print('构造器中定义属性',self.inita)
        print('构造器中定义属性',self.initb)

    def show_all(self):
        print('类属性',self.name)
        print('类属性',self.nameb)

# a = A()
# a.show()
# b = B()
# b.show()
c = C()
c.show_all()