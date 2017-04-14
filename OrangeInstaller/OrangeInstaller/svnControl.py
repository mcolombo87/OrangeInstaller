import sys, os
import subprocess
import getpass
from Functions import functions, systemTools

class svnControl(object):
    """SVN controller. Interface with svnclient."""

    svnRemoteClient = 'svn://svn.openorange.com/' #by default
    svnUserName = 'username'
    svnPassword ='password'

    def __init__ (self, **kwargs):
        self.logon()

    '''Des'''
    def checkout (self, moduleNamePath, revision, svnPath, installRoute):
        currentSystem = systemTools.systemInfo()
        currentSystem = currentSystem[0] #Take first position >> OS Name
        if (currentSystem == 'Windows'):
            svnclientPath = os.path.abspath("svnclient/svn.exe")
            svnclientPath.replace("\\", "/")
        if (currentSystem == 'Linux'):
            svnclientPath = 'svn'
        if (currentSystem != 'Windows' and currentSystem != 'Linux'):
            functions.logging.debug('Error: System not recognized >> {}'.format(currentSystem))
            functions.exitProgram(1) #End with Err
        if (moduleNamePath):
            installRoute += '/'+moduleNamePath
            moduleNamePath.replace("\\", "/")

        construction = (svnclientPath+' checkout'+' -r '+ revision+' --username '+self.svnUserName+' --password ' +self.svnPassword+' '+self.svnRemoteClient+svnPath+
                        ' '+installRoute)
        functions.logging.debug('Send to SVN: {}'.format(construction)) #ONLY FOR PRE-RELEASE VERSION, DELETE LATER (PRINT USERNAME AND PASS FOR SVN)
        moduleInstall = subprocess.Popen(construction, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
        functions.logging.debug('CheckOut Report: {}'.format(moduleInstall.stdout.read()))

    '''Des'''
    def logon (self):
        self.svnUserName = input('SVN Username: ')
        self.svnPassword = getpass.getpass('SVN password: ')

