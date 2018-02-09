#This is a little supply program for easy updating.
try:
    from Functions import functions, systemTools
    import subprocess
except:
    print "Necesary imports Fail, report this issue"

class oiUpdate(object):
    
    def __init__(self, **kwargs):
        config = self.loadConfig()
        self.svnPath = config['svnPath']
        self.svnRemoteClient = config['svnRemoteClient']
        self.svnUser = config['svnUser']
        self.svnPwd = config['svnPwd']
        self.svnclientPath = config['svnclientPath']
        self.osCondition = config['osCondition']
        self.installRoute = config['installRoute']
        self.actualVersion = functions.readConfigFile('System','Version')

    def checkUpdate(self):
        construction = (self.svnclientPath + ' --no-auth-cache --non-interactive -u -q status ' + self.installRoute)
        testingCheckout = subprocess.Popen(construction, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=self.osCondition)
        self.dialogs(10)
        outs, errs = testingCheckout.communicate()
        if outs:
            try:
                outs.index("*")
                self.dialogs(8)
            except:
                self.dialogs(9)
                self.finishUpdate()

    def updateOI(self):
        self.dialogs(4)
        construction = (self.svnclientPath + ' --no-auth-cache --non-interactive cleanup ' + self.installRoute)
        testingCheckout = subprocess.Popen(construction, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=self.osCondition)
        outs, errs = testingCheckout.communicate()
        if outs:
            self.dialogs(5)
        
        self.dialogs(6)
        construction = (self.svnclientPath + ' checkout -r HEAD' + ' --no-auth-cache --force' + ' --username ' + self.svnUser + ' --password ' + self.svnPwd + ' ' + self.svnRemoteClient + self.svnPath +
                        ' ' + '"' + self.installRoute + '"')
        testingCheckout = subprocess.Popen(construction, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=self.osCondition)
        outs, errs = testingCheckout.communicate()
        
        if not errs:
            if outs:
                self.dialogs(2)
        else:
            self.dialogs(3)
            print errs
        self.finishUpdate()

    def finishUpdate(self):
        self.dialogs(7)
        try:
            a = input("")
        except:
            pass
        finally:
            exit()

    def startOI(self):
        pass

    def dialogs(self, nrDialog):
        if nrDialog == 1:
            print "*****************************************************************************"
            print "* OrangeInstaller AutoUpdate                                                *"
            print "* Author: M.Colombo                                                         *"
            print "*****************************************************************************"
            print " "
            print "Welcome to OI Update... please wait while we searching any update for you..."
            print "_____________________________________________________________________________"
        elif nrDialog == 2:
            print "# Finished!! OI is updated to Version: " + self.actualVersion
        elif nrDialog == 3:
            print "# An error has occurred, the update was fail"
        elif nrDialog == 4:
            print "# Cleaning previous updates..."
        elif nrDialog == 5:
            print "# Ready!..."
        elif nrDialog == 6:
            print "# Starting with the update..."
        elif nrDialog == 7:
            print "# Press any key for exit..."
        elif nrDialog == 8:
            print "# Update available..."
        elif nrDialog == 9:
            print "# OI not need update, it's on date..."
        elif nrDialog == 10:
            print "# Searching for updates..."
        else:
            print "An error was ocurred, please report bug in GitHub!"

    def loadConfig(self):
        if systemTools.isWindows():
            svnclientPath = "svnclient\svn.exe"
            installRoute = "TESTUPDATE"
            osCondition = False
        if systemTools.isLinux():
            svnclientPath = "svn"
            installRoute = "TESTUDAPTE"
            osCondition = True
        svnPath = 'oitest'
        svnRemoteClient= 'svn://svn.openorange.com/'
        svnUser = 'oi'
        svnPwd = 'oi'
        return {'svnPath':svnPath, 'svnRemoteClient':svnRemoteClient, 'svnUser':svnUser, 'svnPwd':svnPwd,
            'svnclientPath':svnclientPath, 'installRoute':installRoute, 'osCondition':osCondition}

    def startProgram(self):
        self.dialogs(1)
        self.checkUpdate()
        self.updateOI()

#Starting Program!

oiUpdate = oiUpdate()
oiUpdate.startProgram()

