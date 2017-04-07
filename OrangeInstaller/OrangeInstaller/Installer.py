import dataConnection, svnControl

class Installer(object):
    """This class is main, from here all be initialized. First object created and the last in destroy.
    His primitives are focus in concentrated and management each cycle on the installation"""
    
    def __init__(self, **kwargs):
        self.installPath = self.__setDefaultPath()
        self.dataConnect = dataConnection.dataConnection()

    def setInstallPath (self, path):
        self.installPath = path

    def getInstallPath (self):
        return self.installPath

    '''Des'''
    def initialization(self):
        if (self.dataConnect.testConnection):
            print('Connection to DB: OK')
        else: print('Fail to connect with DB')
        modulesInfo = self.setCompanyModules()
        svn = svnControl.svnControl()
        for a in range(len(modulesInfo)):
            moduleToInstall = modulesInfo[a]
            print ('Installing: '+moduleToInstall[0])
            moduleName = moduleToInstall[0]
            if moduleName == 'repo':
                moduleName = None
            svn.checkout(moduleName, str(moduleToInstall[2]), moduleToInstall[4])

    '''Des'''
    def startInstall(self):
        pass

    '''Des'''
    def __setDefaultPath(self):
        self.installPath = 'C:\OrangeInstaller\Test'

    '''Des'''
    def setCompanyModules(self): #CAMBIAR HARDCODEO DE IDCOMPANY
        modulesInfo = self.dataConnect.getData('modules','1',['module, ', 'level, ', 'revision, ', 'svnurl, ', 'path'])
        # print(modulesInfo) #Test line, delete after
        return modulesInfo