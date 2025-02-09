import math as m

a = {}

a[4] = 9
a["e"] = 4
w = 7
a[w] = "45"
x = 6
y = 4.7
a[str(x)+str(y)] = [8,23,0]
a[1] = "t"
print(a)
print(a.keys())
print(3 in a.keys())
print(a[str(x)+str(y)])
print(a.pop(str(x)+str(y)))
print(a)
