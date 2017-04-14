import dataConnection, svnControl
from Functions import functions, systemTools
from os import path

class Installer(object):
    """This class is main, from here all be initialized. First object created and the last in destroy.
    His primitives are focus in concentrated and management each cycle on the installation"""
   
    modulesInfo = None
    installPath = None
    svn = None

    def __init__(self, **kwargs):
        self.__setDefaultPath()
        self.dataConnect = dataConnection.dataConnection()

    def setInstallPath (self, path):
        self.installPath = path

    def getInstallPath (self):
        return self.installPath

    '''Des'''
    def initialization(self, companyId):
        if (self.dataConnect.testConnection() == True):
            print('Connection to DB: OK')
            functions.logging.debug('Connection to DB: OK')
        else: 
            print('Fail to connect with DB')
            functions.logging.debug('Fail to connect with DB')
        self.setCompanyModules(companyId)

    '''Des'''
    def startInstall(self):
        self.svn = svnControl.svnControl()
        for a in range(len(self.modulesInfo)):
            moduleToInstall = self.modulesInfo[a]
            moduleName = moduleToInstall[0]
            print ('Installing: '+moduleName)
            functions.logging.debug('Installing: {}'.format(moduleName))
            if (moduleName == 'repo' or moduleName == 'DevelopAr'): #THIS SENTENCE IS ONLY FOR TESTING INSTALL WITHOUT INSTALLING ALL. CHANGE LATER
                moduleName = ''
            self.svn.checkout(moduleName, str(moduleToInstall[2]), moduleToInstall[4],self.installPath)
        extraDirPath = self.installPath+'\\extra'
        if (path.isdir(extraDirPath)): #Create __init__.py if exist extra folder and the file is not there
            if(not path.exists(extraDirPath+'\\__init__.py')):
                open(extraDirPath+'\\__init__.py', 'x')

    '''Des'''
    def __setDefaultPath(self):
        systemInfo = systemTools.systemInfo()
        currentSystem = systemInfo[0]
        if (currentSystem == 'Windows'):
            self.setInstallPath('C:\\OpenOrange')
        if (currentSystem == 'Linux'):
            self.setInstallPath('~/OpenOrange')

    '''Des'''
    def setCompanyModules(self, companyId): 
        self.modulesInfo = self.dataConnect.getData('modules',companyId,['module, ', 'level, ', 'revision, ', 'svnurl, ', 'path'])
        functions.logging.debug('DB > Get Data: {}'.format(self.modulesInfo))
        # print(modulesInfo) #Test line, delete after
    

