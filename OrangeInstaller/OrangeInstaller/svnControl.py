import sys, os
import subprocess

class svnControl(object):
    """SVN controller. Interface with svnclient."""

    svnRemoteClient = 'svn://svn.openorange.com/'
    svnUserName = 'username'#modify
    svnPassword = 'password'#modify

    def __init__ (self, **kwargs):
        pass

    '''Des'''
    #svnPath = '/customizations/aerocargas', path=''
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
        print (construction) #Delete Later
        moduleInstall = subprocess.Popen(construction, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #print(moduleInstall.stdout.read()) #For catch output from process, use later for log.

    '''Des'''
    def logon (self):
        pass

