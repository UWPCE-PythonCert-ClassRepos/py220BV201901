"""
recursion for debuging
"""

import sys
from loguru import logger


def my_fun(n):
    logger.debug(f"parameter: {n}")
    # if n == 2:
    #    return True
    # return my_fun(n / 2)
    if n == 0:
        return True
    return my_fun(n // 2)


if __name__ == '__main__':
    logger.enable('__main__')
    logger.info('logger enabled')
    n = int(sys.argv[1])
    logger.debug(my_fun(n))
    # print(my_fun(n))
