import pytest

size = lambda x: x*2

def double(x):
    return x*2

def y(z):
    return (z(10))
    
size2 = double(2)

assert y(double) == y(size)