import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import dataConnection, Installer
from Functions import functions

class userWindow(Gtk.Window):
    """desc"""
    dataConnect = None
    builder = None
    companyId = None
    companyName = None
    
    def __init__(self):
        self.dataConnect = dataConnection.dataConnection()
        self.installation = Installer.Installer() #Instance of Installer class

        self.builder = Gtk.Builder()
        self.builder.add_from_file("./GUI/OrangeInstallerGUI.glade")
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
        self.statusbar1 = self.builder.get_object('statusbar1')
        self.selectorList = self.builder.get_object('treeview-selection')
        self.companyLabel = self.builder.get_object('companyLabel')
        self.installPathLabel = self.builder.get_object('installPathLabel')
        self.folderChooser = self.builder.get_object('folderChooser')
        self.inputSVNUser = self.builder.get_object('inputSVNUser')
        self.inputSVNPassword = self.builder.get_object('inputSVNPassword')
        self.installButton = self.builder.get_object('installButton')

        #check database Status
        dbcheck = self.dataConnect.testConnection()
        if dbcheck:
            self.communicator('Success connecting to database')
        else: self.communicator('Fail to connect with database')

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Company", renderer, text=0)
        self.listview.append_column(column)
		
    def userExit(self, widget):
        functions.exitProgram(2) #End by user
        exit()

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

    def preparateWin1(self):
        self.companyLabel.set_text(self.companyName)
        self.installPathLabel.set_text(self.installation.getInstallPath())

    def prevWindow(self, widget):
        prevWindowPos = self.actualWindowPos - 1
        if (self.actualWindowPos == 2):
            self.win1.hide()
            self.win.show_all()
        if (self.actualWindowPos == 3):
            self.win2.hide()
            self.win.show_all()
        self.actualWindowPos = prevWindowPos #is more clearly
    
    def communicator(self, message):
        if (self.actualWindowPos == 1):
            self.statusbar.push(1,message)
        if (self.actualWindowPos == 2):
            self.statusbar1.push(1,message)

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

    def selectRow(self, widget):
        model, colum = widget.get_selected()
        self.companyName = model[colum][0]

    def changeInstallDirectory(self, widget):
        newPath = self.folderChooser.get_uri().split('file:///')
        newPath = newPath[1] #Discard first split
        self.installation.setInstallPath(newPath)
        self.installPathLabel.set_text(self.installation.getInstallPath())

    def readyToInstall(self, widget):
        if (self.inputSVNUser.get_text_length() !=0 and self.inputSVNPassword.get_text_length() != 0):
            self.installButton.set_opacity(1)
            self.installButton.set_sensitive(True)
        else:
            if (self.installButton.get_sensitive() == True):
                self.installButton.set_opacity(0.5)
                self.installButton.set_sensitive(False)

    def startInstall(self, widget):
        self.nextWindow(widget)
        self.installation.setSvnControlFromOut()
        #FALTA ENVIAR USUARIO Y CONTRASEÑA DE SVN ACA ANTES DE INSTALLAR
        if (self.installation.svn):
            self.installation.startInstall()