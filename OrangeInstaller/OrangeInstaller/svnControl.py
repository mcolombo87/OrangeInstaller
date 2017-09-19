#encoding: utf8
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
            if (kwargs['SVNUsername']):
                self.svnUserName = kwargs['SVNUsername']
            if (kwargs['SVNPassword']):
                self.svnPassword = kwargs['SVNPassword']
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
        self.setSvnCLientPath()
        if (moduleNamePath):
            if (systemTools.isWindows()):
                moduleNamePath = moduleNamePath.replace("/","\\")
                installRoute += '\\'+moduleNamePath
                #installRoute.replace("\\", "/")
            if (systemTools.isLinux()):
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
        if self.svnUserName == 'username':
            self.svnUserName = raw_input(tr("SVN Username: "))
            self.svnPassword = getpass.getpass(tr("SVN Password: "))

    def setSvnCLientPath(self):
        if (systemTools.isWindows()):
            self.svnclientPath = os.path.abspath("svnclient/svn.exe")
            self.svnclientPath.replace("\\", "/")
        if (systemTools.isLinux()):
            self.svnclientPath = 'svn'
        if (not systemTools.isWindows() and not systemTools.isLinux()):
            functions.logging.debug('Error: System not recognized >> {}'.format(currentSystem))
            functions.exitProgram(1) #End with Err


    '''
    DESC= Check credentials for SVN
    IN= None
    OUT= True or False
    '''
    def checkCredentials (self):

        import shlex

        #Set testing
        self.setSvnCLientPath()
        folderCheck = 'checkSVNCred'
        revision = '0'
        svnPath = 'repo'
        installRoute = folderCheck
        if systemTools.isWindows():
            osCondition = False
        if systemTools.isLinux():
            osCondition = True
        #End Set
        construction = (self.svnclientPath + ' --no-auth-cache --non-interactive cleanup ' + '"' + installRoute + '"')
        subprocess.Popen(construction, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=osCondition)
        
        construction = (self.svnclientPath + ' checkout' + ' --no-auth-cache --force' + ' -r ' + revision +' --username ' + self.svnUserName + ' --password ' + self.svnPassword + ' ' + self.svnRemoteClient + svnPath +
                        ' ' + '"' + installRoute + '"')
        testingCheckout = subprocess.Popen(construction, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=osCondition)

        timeout = 0
        outs, errs = '',''
        exit = False

        while timeout < 10 and exit == False:
            print construction
            if testingCheckout.poll() == None:
                time.sleep(0.5)
                timeout += 1
                print(tr("Process haven't finished yet..."))
            else: exit = True

        try:
            if systemTools.isWindows():
                outs, errs = testingCheckout.communicate()
                testingCheckout.terminate()
            if systemTools.isLinux():
                outs, errs = testingCheckout.communicate()
                testingCheckout.terminate()
        except:
            functions.logging.debug(tr("OrangeInstaller cannot validate SVN Username and Password"))
        print outs, errs

        if errs:
            functions.logging.debug(functions.processSVNout(errs))
            return functions.processSVNout(errs)
        else:
            return True
