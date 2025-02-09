'''import seaborn as sns
import pandas as pd'''
import matplotlib.pyplot as plt
import math as m

x = []
y = []
'''
for i in range(0,100):
    x.append(i*0.1)
    y.append(m.sin(x[i]))
'''

def rek(start_population,last_moment,r):
    res = []
    population = []
    moments = []
    rs = []
    n = last_moment
    for i in range(0,last_moment+1):
        moments.append(i)
        if i == 0:
            population.append(start_population)
        else:
            prev = population[i-1]
            pop = r*prev*(1 - prev)
            population.append(pop)
        if population[i] == 0:
            n = i
            break

    rs.append(r) #0
    rs.append(population[n])#1
    rs.append(population[n]-population[n-1])#2
    res.append(moments)
    res.append(population)
    res.append(rs)
    return res

def foo(start_population,last_moment,r_last,step):
    r_s = []
    p_s = []
    result = []
    i = 0
    while i < r_last:
        res = rek(start_population,last_moment,i)
        rs = res[2]
        r_s.append(rs[0])
        p_s.append(rs[1])
        i = i + step
        
    result.append(r_s)
    result.append(p_s)
    return result

result = foo(0.1,50,3,0.01)

print(result[1][len(result[1])-1])

plt.plot(result[0],result[1])
plt.grid(True)
plt.show()
