def apply_twice(f):
    return lambda x:f(f(x))
f = lambda x: x + 3      
g = apply_twice(f)
print(g(2))