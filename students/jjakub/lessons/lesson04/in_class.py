
\
size = lambda x:x*2


def double(x):
    return x * 2


def y(z):
    print(z(10))

assert y(double) == y(size)


an_iterable = ['a', 'b', 'c']
for letter in an_iterable:
    print(letter)

an_iterator = iter(an_iterable)
an_iterator.__next__()
'a'
an_iterator.__next__()
'b'