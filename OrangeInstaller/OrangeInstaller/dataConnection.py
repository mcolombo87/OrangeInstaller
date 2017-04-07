import pymysql
from pymysql import cursors

class dataConnection(object):
    """Management and data flow with program and DBMS"""

    dbEnigne = 'MySQL'
    basename = 'orangeinstaller'
    host = 'localhost'
    port = 3106
    username = 'root'
    password = 'root' #modify
    connector = None
  
    def __init__(self, **kwargs):
        #self.stablishConnection()
        pass

    '''Des'''
    def testConnection(self):
        test = self.stablishConnection()
        if (test):
            return True
        else:
            return False
            self.connector.close()

    '''Des'''
    def stablishConnection(self):
        try:
            self.connector = pymysql.connect(host='127.0.0.1', 
                                    port=3306, 
                                    user='root', 
                                    passwd='1234',
                                    db='mysql')
        except:
            print ('Error when try connect to database')
            return False
        else:
            return True

    '''Des'''
    def getData(self, table, id, columns):
        self.stablishConnection()
        columnsBuild = ''
        for a in range(len(columns)):
            columnsBuild += columns[a]
        print (columnsBuild)
        sql = "SELECT {} FROM {}.{} WHERE idcompany={}".format(columnsBuild, self.basename, table,id)
        cursor = self.connector.cursor()
        cursor.execute(sql)
        data = []
        for a in cursor.fetchall():
            data.append(a)
        return data

    '''Des'''
    def getDataSearch(self, table, field, key):
        #Query here!
        self.stablishConnection()
        sql = "SELECT idcompany, name, skin FROM {}.{} WHERE {} LIKE {}".format(self.basename, table, field, key)
        cursor = self.connector.cursor()
        cursor.execute(sql)
        data = []
        for a in cursor.fetchall():
            data.append(a)
        return data