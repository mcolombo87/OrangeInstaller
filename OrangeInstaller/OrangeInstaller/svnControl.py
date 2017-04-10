import sys, os
import subprocess
import getpass
from Functions import functions

class svnControl(object):
    """SVN controller. Interface with svnclient."""

    svnRemoteClient = 'svn://svn.openorange.com/'
    svnUserName = 'username'
    svnPassword ='password'

    def __init__ (self, **kwargs):
        pass

    '''Des'''
    def checkout (self, moduleNamePath, revision, svnPath, installRoute):
        self.logon()
        svnclientPath = os.path.abspath("svnclient/svn.exe")
        svnclientPath.replace("\\", "/")
        if (moduleNamePath):
            moduleNamePath.replace("\\", "/")
            installRoute += '\\'+moduleNamePath
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
        self.svnUserName = input('SVN Username: ')
        self.svnPassword = getpass.getpass('SVN password: ')

