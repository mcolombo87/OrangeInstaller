import pymysql
from pymysql import cursors
from Functions import functions

tr = functions.tr

class dataConnection(object):
    """Management and data flow with program and DBMS"""

    connector = None

    def __init__(self, **kwargs):
        #All this data is taken from conf.cfg file. It's for stablish conection with DB
        self.dbEnigne = functions.readConfigFile('database','dbEnigne')
        self.basename = functions.readConfigFile('database','basename')
        self.host = functions.readConfigFile('database','host')
        self.port = int(functions.readConfigFile('database','port'))
        self.username = functions.readConfigFile('database','username')
        self.password = functions.readConfigFile('database','password')

    ''' 
    DESC= Test DB Server connection
    IN= None
    OUT= Return True if the connection was successful, or false if wasn't
    '''
    def testConnection(self):
        test = self.stablishConnection()
        if (test):
            functions.logging.debug(tr("Connection to DB: OK"))
            return True
        else:
            functions.logging.debug(tr("Fail to connect with DB"))
            return False

    ''' 
    DESC= Stablish connection with the database.
    IN= None
    OUT= Return True if the connection was successful, or false if something's happened and connection fail
    '''
    def stablishConnection(self):
        try:
            self.connector = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.username,
                                    passwd=self.password,
                                    db=self.basename)
        except:
            functions.logging.debug(tr("Error when try connect to database"))
            print (tr("Error when try connect to database"))
            return False
        else:
            return True

    """
    DESC= Read data from DB. This method was built too generic so required indicate table, key and columns (to show).
        Any error end the execution of the program.
    IN= Table: Table on DB where search data. Id: primary key. Columns: vector that contains columns from select statement.
        This vector must be of the form ["Column1 ,", "Column2"], take specially atention of separator ',' on each columns except in the last.
    OUT= Return a list of all data which match of select statement (data)
    """
    def getData(self, table, id, columns):
        try:
            self.stablishConnection()
            columnsBuild = ''
            for a in range(len(columns)):
                columnsBuild += columns[a]
            sql = "SELECT {} FROM {}.{} WHERE idcompany = {}".format(columnsBuild, self.basename, table, id)
            cursor = self.connector.cursor()
            cursor.execute(sql)
            data = []
            for a in cursor.fetchall():
                data.append(a)
            return data
        except:
            functions.logging.debug("Query ERROR")
            functions.exitProgram(1)

    ''' 
    DESC= Read data from DB. The difference with getData is that this don't send a primary key, work like a searcher of ...
        ...data inside of specific field on "company" table.
        Any error end the execution of the program.
    IN= Table: Table on DB where search data. Field: columns where data is stored. Key: Word to search.
    OUT= Return a list of all data which match of select statement (data)
    '''
    def getDataSearch(self, table, field, key, columns):
        try:
            self.stablishConnection()
            columnsBuild = ''
            for a in range(len(columns)):
                columnsBuild += columns[a]
            sql = "SELECT {} FROM {}.{} WHERE {} LIKE '%{}%'".format(columnsBuild, self.basename, table, field, key)
            cursor = self.connector.cursor()
            cursor.execute(sql)
            data = []
            for a in cursor.fetchall():
                data.append(a)
            return data
        except:
            functions.logging.debug("Query ERROR")
            functions.exitProgram(1)

    ''' 
    DESC= End connection with database
    IN= None
    OUT= None
    '''
    def terminated (self):
        self.connector.close()
