import threading
import subprocess
from Functions import functions

class installThread(threading.Thread):
    construction = None
    shellActive = None

    def __init__(self, const, shellAct, sp, mName, objInstaller):
        threading.Thread.__init__(self)

        self.construction = const
        self.shellActive = shellAct
        self.semaphore = sp
        self.moduleName = mName
        self.objInstaller = objInstaller
        
    def run(self):
        self.objInstaller.pushCheckoutStacks()
        self.semaphore.acquire()
        if (self.moduleName != 0):
            msg = str('Installing: '+self.moduleName)
            if (self.moduleName == ''):
                msg = str('Installing: Base and Standard')
            print (msg)
            functions.logging.debug(msg)
            self.objInstaller.setMsgBuffer(msg)
        functions.logging.debug('Send to SVN: {}'.format(self.construction)) 
        logSVNFileErr = open("svnErr.log", "a")
        report = subprocess.call(self.construction, stdout=logSVNFileOut, stderr=logSVNFileErr)
        functions.logging.debug('SVN Response: {}'.format("Process finished, check svn out for info"))
        logSVNFileOut.close()
        self.semaphore.release()
        self.objInstaller.popCheckoutStacks()
        if (self.objInstaller.getCheckoutStacks() == 0):
            self.objInstaller.createInitExtra()
            self.objInstaller.makeSetting()
