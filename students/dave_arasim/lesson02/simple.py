# simple.py
import logging
log_format = "DKA: %(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
#logging.basicConfig(level=logging.WARNING, format=log_format, filename='simple.log')

formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler('simple.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("DKA: i is 50")

        try:
            print('Out: ', i / (50 - i))
        except ZeroDivisionError:
            logging.error("DKA: Divide by zero. i was {}!".format(i))

if __name__ == "__main__":
    my_fun(100)