import svnControl
import dataConnection
import Installer
from Functions import functions, systemTools

class test(object):
    """
    Class for testing
    """
    def __init__(self):
        pass

    #For test one install module (or two).
    def testModuleCheckout (self, companyId, moduleToTest1, moduleToTest2):
        testObject = Installer.Installer()
        testObject.initialization(companyId) #Remember, initialization parameter is companyId
        svn = svnControl.svnControl()
        svn.logon()
        for a in range(len(testObject.modulesInfo)):
            moduleToInstall = testObject.modulesInfo[a]
            moduleName = moduleToInstall[0]
            if (moduleName == moduleToTest1 or moduleName == moduleToTest2): 
                svn.checkout(moduleName, str(moduleToInstall[2]), moduleToInstall[4],testObject.installPath, testObject)

    def checkSystemTools(self):
        if systemTools.isWindows():
            print "Is windows"
        if systemTools.isLinux():
            print "Is Linux"