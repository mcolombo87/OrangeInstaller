import dataConnection, svnControl, openSettingsMaker
from Functions import functions, systemTools
from os import path
import getpass

class Installer(object):
    """This class is main, from here all be initialized. First object created and the last in destroy.
    His primitives are focus in concentrated and management each cycle on the installation"""
   
    modulesInfo = None
    installPath = None
    svn = None
    msgBuffer = 'Test'

    def __init__(self, **kwargs):
        self.currentSystem = systemTools.systemInfo()
        self.currentSystem = self.currentSystem[0]
        self.__setDefaultPath()
        self.dataConnect = dataConnection.dataConnection()
        self.endInstallControl = False
        self.checkoutStacks = 0

    def setInstallPath (self, path):
        self.installPath = path

    def getInstallPath (self):
        return self.installPath

    def getMsgBuffer(self):
        return self.msgBuffer
    
    def setMsgBuffer(self, msg):
        self.msgBuffer = msg

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
        if (self.svn == None):
            self.svn = svnControl.svnControl()
        for a in range(len(self.modulesInfo)):
            moduleToInstall = self.modulesInfo[a]
            moduleName = moduleToInstall[0]
            # msg = 'Installing: {}'.format(moduleName)
            # print (msg)
            # functions.logging.debug(msg)
            #self.msgBuffer = msg
            if (moduleName == 'repo' or moduleName == 'DevelopAr'): 
                moduleName = ''
            self.svn.checkout(moduleName, str(moduleToInstall[2]), moduleToInstall[4],self.installPath, self)
        # msg = 'Creating Settings.xml'
        # print(msg) #For Console use
        # self.msgBuffer = msg
        # self.settingsMaker()

        # msg = 'Installated in: {}'.format(self.installPath)
        # print(msg)
        # functions.logging.debug(msg)
        # self.msgBuffer(msg)
        # self.endInstallControl = True

    '''Des'''
    def __setDefaultPath(self):
        if(self.currentSystem == 'Windows'):
            self.setInstallPath(functions.readConfigFile('System','DefaultPath')) #Read directory of installation from cfg
        if(self.currentSystem == 'Linux'):
            self.setInstallPath('/home/'+getpass.getuser()+'/'+functions.readConfigFile('System','DefaultPath')) #Ever define folders beyond home/user in cfg file

    '''Des'''
    def setCompanyModules(self, companyId): 
        self.modulesInfo = self.dataConnect.getData('modules',companyId,['module, ', 'level, ', 'revision, ', 'svnurl, ', 'path, ', 'idcompany'])
        msg = 'DB > Get Data: {}'.format(self.modulesInfo)
        functions.logging.debug(msg)
        
    def settingsMaker (self):
        companyInfo = self.dataConnect.getData('company', self.modulesInfo[0][5], [' * ']) #5 for idcompany in vector
        settingsPath = self.installPath+'\\settings\\'
        if (self.currentSystem == 'Linux'):
            settingsPath.replace("\\", "/")
        try:
            outXMLfile = open(settingsPath+'settings.xml','w') #Truncate file if already exist
        except:
            msg = "Can't create Setting.xml"
            print(msg) #Create new file
            functions.logging.debug(msg)
            self.msgBuffer = msg
        openSettingsMaker.openSettingsMaker().createSettings(outXMLfile, self.modulesInfo, companyInfo)
    
    def setSvnControlFromOut(self):
        kwargs = {"Interface":True}
        self.svn = svnControl.svnControl(**kwargs)

    def checkStatus(self):
        if (self.endInstallControl == True):
            return True
        else: return False

    def createInitExtra(self):
        if (self.currentSystem == 'Windows'):
            extraDirPath = self.installPath+'\\extra'
            if (path.isdir(extraDirPath)): #Create __init__.py if exist extra folder and the file is not there
                if(not path.exists(extraDirPath+'\\__init__.py')):
                    open(extraDirPath+'\\__init__.py', 'w')
        if (self.currentSystem == 'Linux'):
            if (path.isdir(self.installPath+'/extra')): #Create __init__.py if exist extra folder and the file is not there
                if(not path.exists(self.installPath+'/extra/__init__.py')):
                    open(self.installPath+'/extra/__init__.py', 'w')

    def makeSetting(self):
        msg = 'Creating Settings.xml'
        print(msg) #For Console use
        self.msgBuffer = msg
        self.settingsMaker()

        msg = str('Installated in: '+self.installPath)
        print(msg)
        functions.logging.debug(msg)
        self.msgBuffer = msg
        self.endInstallControl = True

    def pushCheckoutStacks(self):
        self.checkoutStacks = self.checkoutStacks + 1
    
    def popCheckoutStacks(self):
        self.checkoutStacks = self.checkoutStacks - 1

    def getCheckoutStacks(self):
        return self.checkoutStacks


    

