import threading
import subprocess
from Functions import functions

tr = functions.tr

class installThread(threading.Thread):
    ''' 
    Class on charge of generated threads for each module to send to svnclient.
    Encapsulate each connection in a single thread.
    '''
    construction = None
    logFiles = None

    def __init__(self, const, logFiles, sp, mName, objInstaller):
        threading.Thread.__init__(self)

        self.construction = const #Construction of the sentence to send to process, svnControl build it
        self.logFiles = logFiles #Log files where will saving the process output
        self.semaphore = sp #Semaphore that controller all threads
        self.moduleName = mName #module name to install.
        self.objInstaller = objInstaller #Instance of Installer Class
        if (self.objInstaller.getCurrentSystem() != 'Linux'):
            self.subprocessInfo = subprocess.STARTUPINFO()
            self.subprocessInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  #For don't show console windows in each process call (in windows)

    def run(self):
        self.objInstaller.pushCheckoutStacks()
        self.semaphore.acquire()
        if (self.moduleName != 0):
            msg = str(tr("Installing: ") + self.moduleName)
            if (self.moduleName == ''):
                msg = str(tr("Installing: ") + "Base and Standard")
            print (msg)
            functions.logging.debug(msg)
            self.objInstaller.setMsgBuffer(msg)
        functions.logging.debug('Send to SVN: {}'.format(self.construction))
        print(self.construction)

        if (self.objInstaller.getCurrentSystem() == 'Linux'):
            report = subprocess.call(self.construction, stdout=self.logFiles[0], stderr=self.logFiles[1], shell=True)
        else:
            report = subprocess.call(self.construction, stdout=self.logFiles[0], stderr=self.logFiles[1], startupinfo=self.subprocessInfo)

        functions.logging.debug('SVN Response: {}'.format("Process finished, check svn out for info"))
        self.semaphore.release()
        self.objInstaller.popCheckoutStacks() #pop Stack of threads (if is empty, all checkouts is over)
        if (self.objInstaller.getCheckoutStacks() == 0): #If all checkouts finished...
            self.objInstaller.createInitExtra() #...Make __init__.py in extra folder
            self.objInstaller.makeSetting() #...Make settings.xml
