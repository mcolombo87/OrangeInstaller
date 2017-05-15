import threading
import subprocess
from Functions import functions

class installThread(threading.Thread):
    construction = None
    shellActive = None

    def __init__(self, const, shellAct, sp, mName, objInstaller, operationID):
        threading.Thread.__init__(self)

        self.construction = const
        self.shellActive = shellAct
        self.semaphore = sp
        self.moduleName = mName
        self.objInstaller = objInstaller
        self.operationID = operationID
        
    def run(self):
        self.semaphore.acquire()
        if (self.moduleName != 0):
            msg = str('Installing: '+self.moduleName)
            print (msg)
            functions.logging.debug(msg)
            self.objInstaller.setMsgBuffer(msg)
        functions.logging.debug('Send to SVN: {}'.format(self.construction)) 
        report = subprocess.Popen(self.construction, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=self.shellActive)
        functions.logging.debug('SVN Response: {}'.format(report.stdout.read()))
        report.terminate()
        if (self.operationID == 1):
            self.objInstaller.createInitExtra()
        if (self.operationID == 2):
            self.objInstaller.makeSetting()
        self.semaphore.release()

class statusThread(threading.Thread):

    def __init__(self, installObjec, communicatorObj):
        threading.Thread.__init__(self)
        self.installObject = installObjec
        self.communicatorObject = communicatorObj
        
    def run(self):
        self.communicatorObject.push(1,"test")
        while (self.installObject.checkStatus() == False):
            catchProgress = self.installObject.getMsgBuffer()
            self.communicatorObject.push(1,"test2")
