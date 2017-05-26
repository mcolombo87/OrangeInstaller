import threading
import subprocess
from Functions import functions

class installThread(threading.Thread):
    construction = None
    logFiles = None

    def __init__(self, const, logFiles, sp, mName, objInstaller):
        threading.Thread.__init__(self)

        self.construction = const
        self.logFiles = logFiles
        self.semaphore = sp
        self.moduleName = mName
        self.objInstaller = objInstaller
        self.subprocessInfo = subprocess.STARTUPINFO()
        self.subprocessInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        
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
        report = subprocess.call(self.construction, stdout=self.logFiles[0], stderr=self.logFiles[1], startupinfo=self.subprocessInfo)
        functions.logging.debug('SVN Response: {}'.format("Process finished, check svn out for info"))
        self.semaphore.release()
        self.objInstaller.popCheckoutStacks()
        if (self.objInstaller.getCheckoutStacks() == 0):
            self.objInstaller.createInitExtra()
            self.objInstaller.makeSetting()
