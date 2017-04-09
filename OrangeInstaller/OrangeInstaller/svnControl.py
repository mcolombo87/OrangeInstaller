import sys, os
import subprocess
from Functions import functions

class svnControl(object):
    """SVN controller. Interface with svnclient."""

    svnRemoteClient = 'svn://svn.openorange.com/'
    svnUserName = 'username'#modify
    svnPassword = 'password'#modify

    def __init__ (self, **kwargs):
        pass

    '''Des'''
    def checkout (self, moduleNamePath, revision, svnPath):
        svnclientPath = os.path.abspath("svnclient/svn.exe")
        svnclientPath.replace("\\", "/")
        installPath='c:/test' #Change later
        installRoute = installPath
        if (moduleNamePath):
            moduleNamePath.replace("\\", "/")
            installRoute += '/'+moduleNamePath
            print (installRoute)
        construction = (svnclientPath+' checkout'+' -r '+ revision+' --username '+self.svnUserName+' --password ' +self.svnPassword+' '+self.svnRemoteClient+svnPath+
                        ' '+installRoute)
        #print (construction) #Delete Later
        functions.logging.debug('Send to SVN: {}'.format(construction)) #ONLY FOR PRE-RELEASE VERSION, DELETE LATER (PRINT USERNAME AND PASS FOR SVN)
        moduleInstall = subprocess.Popen(construction, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #print(moduleInstall.stdout.read()) #For catch output from process, use later for log.
        functions.logging.debug('CheckOut Report: {}'.format(moduleInstall.stdout.read()))

    '''Des'''
    def logon (self):
        pass

