import sys, os
import installThread
import threading
import getpass
from Functions import functions, systemTools

class svnControl(object):
    """SVN controller. Interface with svnclient."""

    svnRemoteClient = 'svn://svn.openorange.com/' #by default
    svnUserName = 'username'
    svnPassword ='password'

    def __init__ (self, **kwargs):
        if (not kwargs['Interface']):
            self.logon()
        self.semaphore = threading.BoundedSemaphore(1)

    '''Des'''
    def checkout (self, moduleNamePath, revision, svnPath, installRoute,objInstaller):
        currentSystem = systemTools.systemInfo()
        currentSystem = currentSystem[0] #Take first position >> OS Name
        if (currentSystem == 'Windows'):
            svnclientPath = os.path.abspath("svnclient/svn.exe")
            svnclientPath.replace("\\", "/")
            shellActive = False #CheckLater
            if (moduleNamePath):
                installRoute += '\\'+moduleNamePath
                installRoute.replace("\\", "/")
        if (currentSystem == 'Linux'):
            svnclientPath = 'svn'
            shellActive = True
            if (moduleNamePath):
                installRoute += '/'+moduleNamePath
                installRoute.replace("\\", "/")
        if (currentSystem != 'Windows' and currentSystem != 'Linux'):
            functions.logging.debug('Error: System not recognized >> {}'.format(currentSystem))
            functions.exitProgram(1) #End with Err
        print('Route of install: {}'.format(installRoute))
        #CleanUp
        construction = (svnclientPath+ ' --no-auth-cache --non-interactive cleanup '+installRoute)
        #OperationID sets= 0: Nothing, 1: Extra Install, 2: Base, Repo, Develop install.
        thread = installThread.installThread(construction, shellActive, self.semaphore, 0, objInstaller, 0)
        thread.start()
        #functions.logging.debug('Send to SVN: {}'.format(construction)) 
        #cleanUpReport = subprocess.Popen(construction, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=shellActive)
        #functions.logging.debug('Removing locks: {}'.format(cleanUpReport.stdout.read()))
        #cleanUpReport.terminate()
        #Checkout
        operationID = 0
        if (moduleNamePath == ''):
            operationID = 2
        if (moduleNamePath == 'extra/Develop'):
            operationID = 1
        if (revision == 0 or revision == None or revision == '' or revision == 'NULL'):
            revision = 'HEAD' #Check revision and go to Head if is null, zero, None or empty
        construction = (svnclientPath+' checkout'+' --no-auth-cache --force' +' -r '+ revision+' --username '+self.svnUserName+' --password ' +self.svnPassword+' '+self.svnRemoteClient+svnPath+
                        ' '+installRoute)
        
        print (operationID)
        print(svnPath)
        thread = installThread.installThread(construction, shellActive, self.semaphore, moduleNamePath, objInstaller, operationID)
        thread.start()

        #functions.logging.debug('Send to SVN: {}'.format(construction))#ONLY FOR PRE-RELEASE VERSION, DELETE LATER (PRINT USERNAME AND PASS FOR SVN)
        #moduleInstall = subprocess.Popen(construction, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=shellActive)
        #functions.logging.debug('CheckOut Report: {}'.format(moduleInstall.stdout.read()))
        #moduleInstall.terminate()

    '''Des'''
    def logon (self):
        self.svnUserName = raw_input('SVN Username: ')
        self.svnPassword = getpass.getpass('SVN password: ')

