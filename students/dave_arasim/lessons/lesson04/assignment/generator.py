def my_gen():
    n = 1
    print('first yield')
    yield n
    n += 1
    print('second yield')
    yield n

a = my_gen()
b = next(a)
print('b:', b)
c = next(a)
print('c:', c)

try:
    d = next(a)
    print('d:', d)
except StopIteration:
    print('Iterator exhausted')