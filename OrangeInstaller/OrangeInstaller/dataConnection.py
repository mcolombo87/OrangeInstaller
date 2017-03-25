class dataConnection(object):
    """Management and data flow with program and DBMS"""

    dbEnigne = 'MySQL'
    basename = 'Default'
    host = 'localhost'
    port = 3106
    username = 'root'
    password = 'root'

    def __init__(self, **kwargs):
        pass

    '''Des'''
    def testConnection(self):
        return True

    '''Des'''
    def stablishConnection(self):
        return True

    '''Des'''
    def getData(self, table, id):
        data = []
        return data

    '''Des'''
    def getDataSearch(self, table, field, key):
        data = []
        return data