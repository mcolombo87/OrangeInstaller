import sys, os
import subprocess

class svnControl(object):
    """SVN controller. Interface with svnclient."""

    svnRemoteClient = 'svn://svn.openorange.com/'
    svnUserName = 'username'
    svnPassword = 'password'

    def __init__ (self, **kwargs):
        pass

    '''Des'''
    def checkout (self, revision = 0, svnPath = '/customizations/aerocargas', path=''):
        svnclientPath = os.path.abspath("svnclient/svn.exe")
        svnclientPath = svnPath.replace("\\", "/")
        print(svnPath)
        installPath='c:/test/test2'
        construction = (svnclientPath+' checkout'+' --username '+self.svnUserName+' --password ' +self.svnPassword+' '+self.svnRemoteClient+svnPath+
                        ' '+installPath)
        print (construction)
        moduleInstall = subprocess.Popen(construction, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print(moduleInstall.stdout.read())

    '''Des'''
    def logon (self):
        pass

