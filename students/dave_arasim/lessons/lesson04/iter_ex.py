an_iterable = ['a', 'b', 'c']

an_iterator = iter(an_iterable)
print(an_iterator.__next__())
print(an_iterator.__next__())
print(an_iterator.__next__())
print(an_iterator.__next__())  #Throws error (because iterable is exhausted)
