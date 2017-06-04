import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GLib
import dataConnection, Installer, installThread
from Functions import functions
import os

class userWindow(Gtk.Window):
    """Graphical User Interface. Use GTK3 and glade."""
    dataConnect = None
    builder = None
    companyId = None
    companyName = None
    
    def __init__(self):
        self.dataConnect = dataConnection.dataConnection()
        self.installation = Installer.Installer() #Instance of Installer class

        self.builder = Gtk.Builder()
        path = os.path.dirname(os.path.abspath(__file__))
        gladeFile = path+"\\OrangeInstallerGUI.glade"
        if (self.installation.getCurrentSystem() == 'Linux'):
            gladeFile = path+"/OrangeInstallerGUI.glade"
        self.builder.add_from_file(gladeFile)
        self.handlers = {
            "delete-event": Gtk.main_quit,
            "userExit": self.userExit,
            "nextWindow1": self.nextWindow,
            "searching": self.search,
            "selectRow": self.selectRow,
            "prevWindow": self.prevWindow,
            "changeInstallDirectory": self.changeInstallDirectory,
            "readyToInstall": self.readyToInstall,
            "startInstall": self.startInstall,
            "userFinish": self.userFinished,
        }
        self.builder.connect_signals(self.handlers)
        self.win = self.builder.get_object('window')
        self.win1 = self.builder.get_object('window1')
        self.win2 = self.builder.get_object('window2')

        self.actualWindowPos = 1 #First Windows, this is an index for navigator
        self.win.show_all()
        #load objects for working.
        self.liststore = self.builder.get_object('liststore')
        self.listview = self.builder.get_object('treeview')
        self.statusbar = self.builder.get_object('statusbar')
        self.statusbarInstall = self.builder.get_object('statusbarInstall')
        self.selectorList = self.builder.get_object('treeview-selection')
        self.companyLabel = self.builder.get_object('companyLabel')
        self.installPathLabel = self.builder.get_object('installPathLabel')
        self.folderChooser = self.builder.get_object('folderChooser')
        self.inputSVNUser = self.builder.get_object('inputSVNUser')
        self.inputSVNPassword = self.builder.get_object('inputSVNPassword')
        self.installButton = self.builder.get_object('installButton')
        self.slidesNote = self.builder.get_object('notebook')
        self.finishButton = self.builder.get_object('finishButton')
        self.spinner = self.builder.get_object('spinner1')
        self.installLabel = self.builder.get_object('installLabel')

        #check database Status
        dbcheck = self.dataConnect.testConnection()
        if dbcheck:
            self.communicator('Success connecting to database')
        else: self.communicator('Fail to connect with database')

        #List all results for search and show up in screen
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Company", renderer, text=0)
        self.listview.append_column(column)
		
    """User press exit button"""
    def userExit(self, widget):
        functions.exitProgram(2) #End by user
        sys.exit()
    
    """User press Finish button"""
    def userFinished(self, widget):
        functions.exitProgram(0) #Installation Finished
        sys.exit()

    """For next buttons"""
    def nextWindow(self, widget):
        #check if company was selected
        if (self.companyId == None and self.companyName != None):
            resultOfSearch = self.dataConnect.getDataSearch('company','name',self.companyName)
            self.companyId = resultOfSearch[0][0]
        if (self.companyId == None and self.companyName == None):
            self.communicator("First you must choose a Company")
        else:
            nextWindowPos = self.actualWindowPos + 1
            if (self.actualWindowPos == 1):
                self.win.hide()
                self.installation.initialization(self.companyId) #If company was picked so we initialize installer
                self.preparateWin1()
                self.win1.show_all()
            if (self.actualWindowPos == 2):
                self.win1.hide()
                self.win2.show_all()
            if (self.actualWindowPos == 3):
                self.win2.hide()
                self.win3.show_all()
            self.actualWindowPos = nextWindowPos #is more clearly

    """Show company name in screen and install patch"""
    def preparateWin1(self):
        self.companyLabel.set_text(self.companyName)
        self.installPathLabel.set_text(self.installation.getInstallPath())

    """For previous buttons (return buttons)"""
    def prevWindow(self, widget):
        prevWindowPos = self.actualWindowPos - 1
        if (self.actualWindowPos == 2):
            self.win1.hide()
            self.win.show_all()
        if (self.actualWindowPos == 3):
            self.win2.hide()
            self.win.show_all()
        self.actualWindowPos = prevWindowPos #is more clearly
    
    """Take one message and show in screen"""
    def communicator(self, message):
        if (self.actualWindowPos == 1):
            self.statusbar.push(1,message)
        if (self.actualWindowPos == 3): #thirt screen
            self.statusbarInstall.push(1,message)

    """Engine of search bar. Through this, one company will be selected"""
    def search(self, widget):
        imputTest = widget.get_text()
        resultOfSearch = self.dataConnect.getDataSearch('company','name',imputTest)
        #clear treeView
        self.liststore.clear()
        if (len(resultOfSearch) == 0):
            self.communicator('Company not Found, try again')
        if (len(resultOfSearch) > 1):
            self.communicator("Too many result, select one if it's here")
            for i in range(len(resultOfSearch)):
                if (i > 9):
                    self.communicator("Some result not shown in screen.")
                    break
                self.liststore.append([resultOfSearch[i][1]])
        if (len(resultOfSearch) == 1):
            self.liststore.append([resultOfSearch[0][1]])
            self.communicator("Company Chosen")
            self.companyId = resultOfSearch[0][0] #[0] for unique row, [0] for Id
            self.companyName = resultOfSearch[0][1]

    """For pick company from list on screen"""
    def selectRow(self, widget):
        model, colum = widget.get_selected()
        self.companyName = model[colum][0]

    """If directory path change, this set the new one"""
    def changeInstallDirectory(self, widget):
        newPath = self.folderChooser.get_uri().split('file:///')
        newPath = newPath[1] #Discard first split
        newPath = newPath.replace("%20", " ") #Fix spaces
        self.installation.setInstallPath(newPath)
        self.installPathLabel.set_text(self.installation.getInstallPath())

    """Check if the conditions for starting installation are ready or not"""
    def readyToInstall(self, widget):
        if (self.inputSVNUser.get_text_length() !=0 and self.inputSVNPassword.get_text_length() != 0):
            self.installButton.set_opacity(1)
            self.installButton.set_sensitive(True)
        else:
            if (self.installButton.get_sensitive() == True):
                self.installButton.set_opacity(0.5)
                self.installButton.set_sensitive(False)

    """Start all installation Engine"""
    def startInstall(self, widget):
        self.nextWindow(widget)
        self.installation.setSvnControlFromOut()
        self.installation.svn.svnUserName = self.inputSVNUser.get_text()
        self.installation.svn.svnPassword = self.inputSVNPassword.get_text()
        self.installation.startInstall()
        self.installStatus()
        self.checkProgress()

    """Restart refresh timer"""
    def installStatus(self):
        timeout = GObject.timeout_add(10000, self.imagesSlides)

    """This is for refresh status of installation and show it on screen"""
    def checkProgress(self): #decrept
        GObject.timeout_add(1000, self.checkProgress)
        catchProgress = self.installation.getMsgBuffer()
        self.communicator(catchProgress)
    
    """Pass images over installation while wait it"""
    def imagesSlides(self):
        if (self.slidesNote.get_current_page() == (self.slidesNote.get_n_pages() - 1) ):
            self.slidesNote.set_current_page(0)  # back to first picture
        else: self.slidesNote.next_page()
        if(self.installation.checkStatus() == True):
            self.finishButton.set_opacity(1)
            self.finishButton.set_sensitive(True)
            self.spinner.stop()
            self.installLabel.set_text('Installation Finished')
        else: self.installStatus()