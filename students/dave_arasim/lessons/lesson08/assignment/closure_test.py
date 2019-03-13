def counter(start=0):
    count = start
    def increment():
        nonlocal count
        count += 1
        return count
    return increment


def make_multipler(n):
    def multiply(x):
        return x * n
    return multiply


mycounter = counter()
print('1st mycounter():', mycounter())
print('2nd mycounter():', mycounter())
print('3rd mycounter():', mycounter())

print()

mycounter99 = counter(99)
print('1st mycounter99():', mycounter99())
print('2nd mycounter99():', mycounter99())
print('3rd mycounter99():', mycounter99())

print()

mymult3 = make_multipler(3)
print('mymult3(4):', mymult3(4))

print()

mymult5 = make_multipler(5)
print('mymult5(4):', mymult5(4))
