class Installer(object):
    """This class is main, from here all be initialized. First object created and the last in destroy.
    His primitives are focus in concentrated and management each cycle on the installation"""
    
    self.installPath = __setDefaultPath

    def __init__(self, **kwargs):
        pass

    def setInstallPath (self, path):
        self.installPath = path

    def getInstallPath (self):
        return self.installPath

    '''Des'''
    def initialization(self):
        pass

    '''Des'''
    def startInstall(self):
        pass
    '''Des'''
    def __setDefaultPath(self):
        self.installPath = 'C:\OrangeInstaller\Test'
