class A:
    def print_smile(self):
        print (":P)")

class B(A):
    pass

class C(A):
    def print_smile(self):
        print(":(")

class D(B,C):

    pass
#
my_var = C()
my_var.print_smile()
# Пошук атрибутів у класах батьках, завжди йде зліва направо, і знизу вгору

my_var1 = D()
my_var1.print_smile()
print(D.mro())
print(C.mro())
