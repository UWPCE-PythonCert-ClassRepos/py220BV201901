def logged_func(func):
    def logged(*args, **kwargs):
        print("Function {} called".format(func.__name__))
        if args:
            print("\twith args: {}".format(args))
        if kwargs:
            print("\twith kwargs: {}".format(kwargs))
        result = func(*args, **kwargs)
        print("\t Result --> {}".format(result))
        return result
    return logged

def add(a, b, i=0):
    return a + b + i

logging_add = logged_func(add)
print('logging_add: ', logging_add(2000, 111, i=1))
print()

@logged_func
def decorator_add(a, b, i=0):
    return a + b + i

print('decorator_add: ', decorator_add(2000, 111, i=1))
