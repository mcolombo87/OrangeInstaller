import sys, os
import installThread
import threading
import getpass
from Functions import functions, systemTools

class svnControl(object):
    """SVN controller. Interface with svnclient."""

    svnRemoteClient = 'svn://svn.openorange.com/' #by default, is the repository of take
    svnUserName = 'username' #SVN username
    svnPassword ='password' #SVN password

    def __init__ (self, **kwargs):
        if (not kwargs['Interface']):
            self.logon()
        self.semaphore = threading.BoundedSemaphore(1) #Semaphore for thread control (used in installThread))

    ''' 
    DESC= Build svn command and create a process for it execute, first to cleanup later to checkout. Start a new thread for each command.
    IN= ModuleNamePath: Name to module to install (afip, ar, repo, etc).
        revision: svn repository revision
        svnPath: svn route within repository (eg /extra/Develop, /ar.repo)
        installRoute: destination path
        objInstaller: Instance of Installer class
    OUT= None
    '''   
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

        thread = installThread.installThread(construction, shellActive, self.semaphore, 0, objInstaller)
        thread.start()

        if (revision == 0 or revision == None or revision == '' or revision == 'NULL'):
            revision = 'HEAD' #Check revision and go to Head if is null, zero, None or empty
        construction = (svnclientPath+' checkout'+' --no-auth-cache --force' +' -r '+ revision+' --username '+self.svnUserName+' --password ' +self.svnPassword+' '+self.svnRemoteClient+svnPath+
                        ' '+installRoute)
        
        thread = installThread.installThread(construction, shellActive, self.semaphore, moduleNamePath, objInstaller)
        thread.start()

        #functions.logging.debug('Send to SVN: {}'.format(construction))#ONLY FOR PRE-RELEASE VERSION, DELETE LATER (PRINT USERNAME AND PASS FOR SVN)
        #moduleInstall = subprocess.Popen(construction, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=shellActive)
        #functions.logging.debug('CheckOut Report: {}'.format(moduleInstall.stdout.read()))
        #moduleInstall.terminate()

    ''' 
    DESC= set credentials for SVN
    IN= None
    OUT= None
    '''   
    def logon (self):
        self.svnUserName = raw_input('SVN Username: ')
        self.svnPassword = getpass.getpass('SVN password: ')

