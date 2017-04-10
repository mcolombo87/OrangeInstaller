import pymysql
from pymysql import cursors
from Functions import functions

class dataConnection(object):
    """Management and data flow with program and DBMS"""

    connector = None
  
    def __init__(self, **kwargs):
        self.dbEnigne = functions.readConfigFile('database','dbEnigne')
        self.basename = functions.readConfigFile('database','basename')
        self.host = functions.readConfigFile('database','host')
        self.port = int(functions.readConfigFile('database','port'))
        self.username = functions.readConfigFile('database','username')
        self.password = functions.readConfigFile('database','password')

    '''Des'''
    def testConnection(self):
        test = self.stablishConnection()
        if (test):
            functions.logging.debug('Connection to DB: OK')
            return True
        else:
            functions.logging.debug('Fail to connect with DB')
            return False
            

    '''Des'''
    def stablishConnection(self):
        try:
            self.connector = pymysql.connect(host=self.host, 
                                    port=self.port, 
                                    user=self.username, 
                                    passwd=self.password,
                                    db=self.dbEnigne)
        except:
            functions.logging.debug('Error when try connect to database')
            print ('Error when try connect to database')
            return False
        else:
            return True

    '''Des'''
    def getData(self, table, id, columns):
        try:
            self.stablishConnection()
            columnsBuild = ''
            for a in range(len(columns)):
                columnsBuild += columns[a]
            #print (columnsBuild) Delete Later
            sql = "SELECT {} FROM {}.{} WHERE idcompany={}".format(columnsBuild, self.basename, table,id)
            cursor = self.connector.cursor()
            cursor.execute(sql)
            data = []
            for a in cursor.fetchall():
                data.append(a)
            return data
        except:
            functions.logging.debug('Query ERROR')
            functions.exitProgram(1)

    '''Des'''
    def getDataSearch(self, table, field, key):
        try:
            self.stablishConnection()
            sql = "SELECT idcompany, name, skin FROM {}.{} WHERE {} LIKE '%{}%'".format(self.basename, table, field, key)
            cursor = self.connector.cursor()
            cursor.execute(sql)
            data = []
            for a in cursor.fetchall():
                data.append(a)
            return data
        except:
            functions.logging.debug('Query ERROR')
            functions.exitProgram(1)