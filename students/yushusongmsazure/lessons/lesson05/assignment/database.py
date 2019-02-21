from pymongo import MongoClient

class MongoDBConnection(object):
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """
        be sure to use the ip address not name for local windows
        CAUTION: Don't do this in production!!!
        """
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """
        Setup connection to mongoDB
        """
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the connection
        """
        self.connection.close()
