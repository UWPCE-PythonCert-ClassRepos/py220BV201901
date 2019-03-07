from linear import linear
from parallel import parallel

from models import util_drop_all
from database import Connection

def main():
    """
    Ensure you application will create an empty database if one doesn’t exist
    when the app is first run. Call it customers.db
    """
    with Connection():
        util_drop_all()

    linear()

    with Connection():
        util_drop_all()

    parallel()

if  __name__ == '__main__':
    main()
