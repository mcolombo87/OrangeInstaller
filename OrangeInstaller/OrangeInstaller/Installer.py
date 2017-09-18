import dataConnection, svnControl, openSettingsMaker
from Functions import functions, systemTools
from os import path
import getpass

tr = functions.tr

class Installer(object):
    """
    This class is main, from here all be initialized. First object created and the last in destroy.
    His primitives are focus in concentrated and management each cycle on the installation
    """

    modulesInfo = None #List of each module to install, this info it's contained in DB
    installPath = None #Directory of installation
    svn = None #svnControl Class
    msgBuffer = '' #This is a buffer for each message, next these are captured by the user interface to display on screen

    def __init__(self, **kwargs):
        self.currentSystem = systemTools.osName()
        self.__setDefaultPath()
        self.dataConnect = dataConnection.dataConnection()
        self.endInstallControl = False #Flag for indicate if the installation finished or not
        self.checkoutStacks = 0 #This is an important counter, increment your value for each checkout in queue, the real control for determinated if the installation...
                                #...finished or not is through this. Once this count started, will return to cero when the installation is over.
        # in case createShortcut or openConsole haven't been initialized (advanced options, only in GUI)
        if not hasattr(self, "createShortcut"):
            self.createShortcut = True
        if not hasattr(self, "openConsole"):
            self.openConsole = False

    def setInstallPath (self, path, companyName=""):
        if(systemTools.isLinux()):
            self.installPath = path + "/" + companyName if companyName else path
        else:
            self.installPath = path + "/" + companyName if companyName else path

    def getInstallPath (self):
        return self.installPath

    def getMsgBuffer(self):
        return self.msgBuffer

    def setMsgBuffer(self, msg):
        self.msgBuffer = msg

    ''' 
    DESC= This is the first kick of the install process, test connection to DB and it set each module to install.
    IN= companyId: id of Company to install, the value is the primary key of company for catch his modules (in DB).
    OUT= Nothing return
    '''
    def initialization(self, companyId):
        if (self.dataConnect.testConnection() == True):
            print(tr("Connection to DB: OK"))
            functions.logging.debug(tr("Connection to DB: OK"))
        else: 
            print(tr("Fail to connect with DB"))
            functions.logging.debug(tr("Fail to connect with DB"))
        self.setCompanyModules(companyId)

    ''' 
    DESC= If svnControl object is not instanced, he do it. Then catch each module info, extract data and send to svnControl for make checkout
    IN= None
    OUT= Nothing return
    '''
    def startInstall(self):
        if (self.svn == None):
            self.svn = svnControl.svnControl()
        for a in range(len(self.modulesInfo)):
            moduleToInstall = self.modulesInfo[a]
            moduleName = moduleToInstall[0]
            if (moduleName == 'repo' or moduleName == 'DevelopAr'):
                moduleName = ''
            self.svn.checkout(moduleName, str(moduleToInstall[2]), moduleToInstall[4], self.installPath, self)

    '''
    DESC= Set default installation path reading from conf.cfg file
    IN= None
    OUT= Nothing return
    '''
    def __setDefaultPath(self):
        if(self.currentSystem == 'Windows'):
            self.setInstallPath(functions.readConfigFile('System','DefaultPath')) #Read directory of installation from cfg
        if(self.currentSystem == 'Linux'):
            self.setInstallPath('/home/'+getpass.getuser()+'/'+functions.readConfigFile('System','DefaultPath')) #Ever define folders beyond home/user in cfg file

    def setCompanyModules(self, companyId): 
        self.modulesInfo = self.dataConnect.getData('modules',companyId,['module, ', 'level, ', 'revision, ', 'svnurl, ', 'path, ', 'idcompany'])
        msg = 'DB > Get Data: {}'.format(self.modulesInfo)
        functions.logging.debug(msg)

    '''
    DESC= This function create file that will be the setting.xml file and call the xml constructor
    IN= None
    OUT= Nothing return
    '''
    def settingsMaker(self):
        companyInfo = self.dataConnect.getData('company', self.modulesInfo[0][5], [' * ']) #5 for idcompany in vector
        settingsPath = self.installPath + '\\settings\\'
        if (self.currentSystem == 'Linux'):
            settingsPath = self.installPath + '/settings/'
        try:
            outXMLfile = open(settingsPath + 'settings.xml', 'w') #Truncate file if already exist
            openSettingsMaker.openSettingsMaker().createSettings(outXMLfile, self.modulesInfo, companyInfo)
        except:
            msg = tr("Can't create settings.xml")
            print(msg) #Create new file
            functions.logging.debug(msg)
            self.msgBuffer = msg

    ''' 
    DESC= GUI use this function for instancing svnControl and passing an signal for avoid call SVN logon (method of svnControl). 
    On this way, GUI can controlate login through your own interface.
    IN= None
    OUT= Nothing return
    '''  
    def setSvnControlFromOut(self):
        kwargs = {"SVNUsername": None, "SVNPassword": None, "Interface":True}
        self.svn = svnControl.svnControl(**kwargs)

    ''' DESC= Console way to input svn username and password '''
    def setSvnControlLogon(self, svnUsername, svnPassword):
        kwargs = {"SVNUsername": svnUsername, "SVNPassword": svnPassword, "Interface": False}
        self.svn = svnControl.svnControl(**kwargs)

    ''' 
    DESC= Check if installation is over. Is basically a 'get' of endInstallControl, i don't know why i did it... je.
    IN= None
    OUT= True or False, 
    '''  
    def checkStatus(self):
        if (self.endInstallControl == True):
            return True
        else: return False

    ''' 
    DESC= When run a installation of some extras (and not all folder), __init__ file doesn't exist. This do make it.
    IN= None
    OUT= None
    '''  
    def createInitExtra(self):
        if (systemTools.isWindows()):
            extraDirPath = self.installPath + '\\extra'
            if (path.isdir(extraDirPath)): #Create __init__.py if exist extra folder and the file is not there
                if(not path.exists(extraDirPath + '\\__init__.py')):
                    open(extraDirPath + '\\__init__.py', 'w')
        if (systemTools.isLinux()):
            if (path.isdir(self.installPath + '/extra')): #Create __init__.py if exist extra folder and the file is not there
                if(not path.exists(self.installPath + '/extra/__init__.py')):
                    open(self.installPath + '/extra/__init__.py', 'w')

    ''' 
    DESC= Work more as "end installation step". Call to "settings maker" and change endInstallationFlag to True. Installer will be done after that
    IN= None
    OUT= Nothing return
    '''
    def makeSetting(self):
        msg = tr("Creating settings.xml")
        print(msg) #For Console use
        self.msgBuffer = msg
        self.settingsMaker()

        msg = str(tr("Installated in: ") + self.installPath)
        print(msg)
        functions.logging.debug(msg)
        self.msgBuffer = msg
        self.endInstallControl = True

    ''' 
    DESC= Push increment counter and Pop decrement his value
    '''   
    def pushCheckoutStacks(self):
        self.checkoutStacks = self.checkoutStacks + 1

    def popCheckoutStacks(self):
        self.checkoutStacks = self.checkoutStacks - 1

    def getCheckoutStacks(self):
        return self.checkoutStacks

    def getCurrentSystem(self):
        return self.currentSystem

    ''' for Windows only '''
    def makeShortcut(self):
        if systemTools.isWindows() and self.createShortcut:
            import winshell
            if self.openConsole:
                console = "--console"
            else:
                console = ""
            target = self.installPath + "\\OpenOrange.exe"

            desktop = winshell.desktop()
            winshell.CreateShortcut (
                   Path=path.join(desktop, 'OpenOrange.lnk'),StartIn=self.installPath,
                   Target=target,Icon=(target,0),Arguments=console)
