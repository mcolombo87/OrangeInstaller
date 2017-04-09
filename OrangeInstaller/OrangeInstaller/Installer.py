import dataConnection, svnControl

class Installer(object):
    """This class is main, from here all be initialized. First object created and the last in destroy.
    His primitives are focus in concentrated and management each cycle on the installation"""
   
    modulesInfo = None

    def __init__(self, **kwargs):
        self.installPath = self.__setDefaultPath()
        self.dataConnect = dataConnection.dataConnection()
        self.svn = svnControl.svnControl()

    def setInstallPath (self, path):
        self.installPath = path

    def getInstallPath (self):
        return self.installPath

    '''Des'''
    def initialization(self, companyId):
        if (self.dataConnect.testConnection()):
            print('Connection to DB: OK')
        else: print('Fail to connect with DB')
        self.setCompanyModules(companyId)

    '''Des'''
    def startInstall(self):
        for a in range(len(self.modulesInfo)):
            moduleToInstall = self.modulesInfo[a]
            print ('Installing: '+moduleToInstall[0])
            moduleName = moduleToInstall[0]
            if moduleName == 'repo': #THIS SENTENCE IS ONLY FOR TESTING INSTALL WITHOUT INSTALLING ALL. CHANGE LATER
                moduleName = None
            else:
                self.svn.checkout(moduleName, str(moduleToInstall[2]), moduleToInstall[4])

    '''Des'''
    def __setDefaultPath(self):
        self.installPath = 'C:\OrangeInstaller\Test'

    '''Des'''
    def setCompanyModules(self, companyId): 
        self.modulesInfo = self.dataConnect.getData('modules',companyId,['module, ', 'level, ', 'revision, ', 'svnurl, ', 'path'])
        # print(modulesInfo) #Test line, delete after