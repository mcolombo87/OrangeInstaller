import sys, os
import installThread
import subprocess
import time
import threading
import getpass
from Functions import functions, systemTools

tr = functions.tr

class svnControl(object):
    """SVN controller. Interface with svnclient."""

    svnRemoteClient = 'svn://svn.openorange.com/' #by default, is the repository of take
    svnUserName = 'username' #SVN username
    svnPassword ='password' #SVN password

    def __init__ (self, **kwargs):
        if(kwargs):
            if (not kwargs['Interface']):
                self.logon()
        else: self.logon()
        self.semaphore = threading.BoundedSemaphore(1) #Semaphore for thread control (used in installThread))
        self.logSVNFileErr = open("svnErr.log", "w")
        self.logSVNFileOut = open("svnOut.log", "w")
        self.svnclientPath = ''

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
        self.setSvnCLientPath()
        if (moduleNamePath):
            if (currentSystem == 'Windows'):
                moduleNamePath = moduleNamePath.replace("/","\\")
                installRoute += '\\'+moduleNamePath
                #installRoute.replace("\\", "/")
            if (currentSystem == 'Linux'):
                installRoute += '/' + moduleNamePath

        print(tr("Route of install: ") + "{}".format(installRoute))
        logFiles = (self.logSVNFileOut, self.logSVNFileErr)
        #CleanUp
        construction = (self.svnclientPath + ' --no-auth-cache --non-interactive cleanup ' + '"' + installRoute + '"')

        thread = installThread.installThread(construction, logFiles, self.semaphore, 0, objInstaller)
        thread.start()

        if (revision == 0 or revision == '0' or revision == None or revision == '' or revision == 'NULL'):
            revision = 'HEAD' #Check revision and go to Head if is null, zero, None or empty
        construction = (self.svnclientPath + ' checkout' + ' --no-auth-cache --force' + ' -r ' + revision +' --username ' + self.svnUserName + ' --password ' + self.svnPassword + ' ' + self.svnRemoteClient + svnPath +
                        ' ' + '"' + installRoute + '"')

        thread = installThread.installThread(construction, logFiles, self.semaphore, moduleNamePath, objInstaller)
        thread.start()

    ''' 
    DESC= set credentials for SVN
    IN= None
    OUT= None
    '''   
    def logon (self):
        self.svnUserName = raw_input('SVN Username: ')
        self.svnPassword = getpass.getpass('SVN password: ')

    def setSvnCLientPath(self):
        currentSystem = systemTools.systemInfo()
        currentSystem = currentSystem[0] #Take first position >> OS Name
        if (currentSystem == 'Windows'):
            self.svnclientPath = os.path.abspath("svnclient/svn.exe")
            self.svnclientPath.replace("\\", "/")
        if (currentSystem == 'Linux'):
            self.svnclientPath = 'svn'
        if (currentSystem != 'Windows' and currentSystem != 'Linux'):
            functions.logging.debug('Error: System not recognized >> {}'.format(currentSystem))
            functions.exitProgram(1) #End with Err
        

    ''' 
    DESC= Check credentials for SVN
    IN= None
    OUT= True or False 
    ''' 
    def checkCredentials (self):
        #Set testing
        self.setSvnCLientPath()
        folderCheck = 'checkSVNCred'
        revision = '0'
        svnPath = 'afip'
        installRoute = folderCheck

        checkOutFile = open("checkSVN.oins", "w")
        #End Set
        construction = (self.svnclientPath + ' checkout' + ' --no-auth-cache --force' + ' -r ' + revision +' --username ' + self.svnUserName + ' --password ' + self.svnPassword + ' ' + self.svnRemoteClient + svnPath +
                        ' ' + '"' + installRoute + '"')
        testingCheckout = subprocess.Popen(construction, stdout=checkOutFile,stderr=checkOutFile)#subprocess.check_output(construction, stderr=subprocess.STDOUT, shell=False, universal_newlines=False)

        time.sleep(2)
        checkOutFile.close()
        buffer = ''
        #checkOutFile.close()
        #checkOutFile = open("checkSVN.oins", "r")
        checkOutFile = open("checkSVN.oins", "r")
        while buffer == '' or not buffer:
            print("Still working...")
            buffer = checkOutFile.read()
            print (buffer)
            time.sleep(0.5)
        checkOutFile.close()
        if "Checked out revision 0" in buffer:
            return True
        else: 
            return False
        

