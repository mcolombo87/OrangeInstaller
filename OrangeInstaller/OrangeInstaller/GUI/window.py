import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GLib
import dataConnection, Installer, installThread
from Functions import functions, systemTools
import os

tr = functions.tr

class userWindow(Gtk.Window):
    """Graphical User Interface. Use GTK3 and glade."""
    dataConnect = None
    builder = None
    companyId = None
    companyName = None
    codeToSearch = None
    userCodeFlag = False

    def __init__(self):
        self.dataConnect = dataConnection.dataConnection()
        self.installation = Installer.Installer() #Instance of Installer class

        self.builder = Gtk.Builder()
        path = os.path.dirname(os.path.abspath(__file__))
        gladeFile = path + "\\OrangeInstallerGUI.glade"
        if (self.installation.getCurrentSystem() == 'Linux'):
            gladeFile = path + "/OrangeInstallerGUI.glade"
        self.builder.add_from_file(gladeFile)
        # translate window's labels
        for obj in self.builder.get_objects():
            if obj.find_property("placeholder_text") and obj.get_property("placeholder_text"):
                obj.set_property("placeholder_text", tr(obj.get_property("placeholder_text")))
            elif obj.find_property("label") and obj.get_property("label"):
                obj.set_property("label", tr(obj.get_property("label")))
            elif obj.find_property("text") and obj.get_property("text"):
                obj.set_property("text", tr(obj.get_property("text")))

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
            "messageOk" : self.hideMessage,
            "showAdvOpt": self.showOrHideAdvOpt,
            "initialClick": self.initialClick,
            "insertCode":self.insertCode,
            "shortcutButtonToggled": self.shortcutButtonToggled
        }
        self.builder.connect_signals(self.handlers)
        #load objects for working.
        objects = ["initialwindow", "window", "window1", "window2", "message", "treeview", "liststore", \
        "statusbar", "statusbarInstall", "treeview-selection", "companyLabel", "installButton", \
        "installPathLabel", "folderChooser", "inputSVNUser", "inputSVNPassword", "notebook", \
        "finishButton", "spinner1", "installLabel", "revadvoptions", "codebox", "initial", \
        "opt1install", "opt2svn", "opt3report","opt4shortcut", "opt5console", "advoptions", "messagebar", "opt6companyname"]
        # 'buttton1' is Previus button.

        for obj in objects:
            setattr(self, obj, self.builder.get_object(obj))
        
        self.advOptInitial()
        
        self.actualWindowPos = 0 #First window, this is an index for navigator
        self.initialwindow.show_all()
        #self.window.show_all()

        #check database Status
        dbcheck = self.dataConnect.testConnection()
        if dbcheck:
            self.communicator(tr("Connection to DB: OK"))
            self.messagebar.set_text(tr("Connection to DB: OK"))
        else: 
            self.communicator(tr("Fail to connect with DB"))
            self.messagebar.set_text(tr("Fail to connect with DB"))

        #List all results for search and show up in screen
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Company", renderer, text=0)
        self.treeview.append_column(column)

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
            resultOfSearch = self.dataConnect.getDataSearch('company', 'name', self.companyName, "*")
            self.companyId = resultOfSearch[0][0]
        if (self.companyId == None and self.companyName == None):
            self.communicator(tr("First you must choose a Company"))
        else:
            nextWindowPos = self.actualWindowPos + 1
            if (self.actualWindowPos == 1):
                self.installation.setInstallPath(self.installation.getInstallPath(), self.companyName)
                self.window.hide()
                self.installation.initialization(self.companyId) #If company was picked so we initialize installer
                self.preparateWin1()
                self.window1.show_all()
            if (self.actualWindowPos == 2):
                self.window1.hide()
                self.window2.show_all()
            if (self.actualWindowPos == 3): #THIS WINDOWS IS NOT EXIST YET!! 
                self.window2.hide()
                self.window3.show_all()
            self.actualWindowPos = nextWindowPos #is more clearly

    """Show company name in screen and install patch"""
    def preparateWin1(self):
        self.companyLabel.set_text(self.companyName)
        self.installPathLabel.set_text(tr("Default Path: ") + self.installation.getInstallPath())

    """For previous buttons (return buttons)"""
    def prevWindow(self, widget):
        prevWindowPos = self.actualWindowPos - 1
        if (self.actualWindowPos == 2):
            self.window1.hide()
            if self.userCodeFlag == True: #If code user was loaded, the system never shows the search company window
                self.initialwindow.show_all()
            else:
                self.window.show_all()
        if (self.actualWindowPos == 3):
            self.window2.hide()
            self.window.show_all()
        self.actualWindowPos = prevWindowPos #is more clearly

    """Take one message and show in screen"""
    def communicator(self, message):
        if (self.actualWindowPos == 1):
            self.statusbar.push(1, message)
        if (self.actualWindowPos == 3): #third screen
            self.statusbarInstall.push(1, message)

    """Engine of search bar. Through this, one company will be selected"""
    def search(self, widget):
        imputTest = widget.get_text()
        resultOfSearch = self.dataConnect.getDataSearch('company', 'name', imputTest, "*")
        #clear treeView
        self.liststore.clear()
        if (len(resultOfSearch) == 0):
            self.communicator(tr("Company not Found, try again"))
        if (len(resultOfSearch) > 1):
            self.communicator(tr("Too many results, choose one from this list"))
            for i in range(len(resultOfSearch)):
                if (i > 9):
                    self.communicator(tr("Some result not shown in screen."))
                    break
                self.liststore.append(["id: %i - %s" % (resultOfSearch[i][0], resultOfSearch[i][1])])
        if (len(resultOfSearch) == 1):
            self.liststore.append([resultOfSearch[0][1]])
            self.communicator(tr("Company Chosen"))
            self.companyId = resultOfSearch[0][0] #[0] for unique row, [0] for Id
            self.companyName = resultOfSearch[0][1]

    """For pick company from list on screen"""
    def selectRow(self, widget):
        model, colum = widget.get_selected()
        if model and colum:
            if len(model[colum][0].split(" ")) > 1:
                self.companyId = model[colum][0].split(" ")[1]
                self.companyName = model[colum][0].split(" ")[-1]
            else:
                self.companyName = model[colum][0]

    """If directory path change, this set the new one"""
    def changeInstallDirectory(self, widget):
        if systemTools.isWindows():
            newPath = self.folderChooser.get_uri().split('file:///')
        else: newPath = self.folderChooser.get_uri().split('file://')
        newPath = newPath[1] #Discard first split
        newPath = newPath.replace("%20", " ") #Fix spaces
        self.installation.setInstallPath(newPath)
        self.installPathLabel.set_text(tr("Install Path: ") + self.installation.getInstallPath())

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
        self.installPathLabel.set_text(tr("Checking Username and Password from SVN"))
        self.installation.setSvnControlFromOut()
        self.installation.svn.svnUserName = self.inputSVNUser.get_text()
        self.installation.svn.svnPassword = self.inputSVNPassword.get_text()

        if self.installation.svn.checkCredentials() == True:
            self.installPathLabel.set_text(tr("Great Success!"))
            self.nextWindow(widget)
            if self.userCodeFlag:
                self.initialwindow.hide()
            self.installation.startInstall()
            self.installStatus()
            self.checkProgress()
        else:
            self.installPathLabel.set_text(tr(self.installation.svn.checkCredentials()))
            # translate secondary text here
            self.message.set_property("secondary_text", tr(self.message.get_property("secondary_text")))
            self.message.show_all()

    """Restart refresh timer"""
    def installStatus(self):
        timeout = GObject.timeout_add(10000, self.imagesSlides)

    """This is for refresh status of installation and show it on screen (DECREPT)"""
    def checkProgress(self): 
        GObject.timeout_add(1000, self.checkProgress)
        catchProgress = self.installation.getMsgBuffer()
        self.communicator(catchProgress)

    """Pass images over installation while wait it"""
    def imagesSlides(self):
        if (self.notebook.get_current_page() == (self.notebook.get_n_pages() - 1) ):
            self.notebook.set_current_page(0)  # back to first picture
        else: self.notebook.next_page()
        if(self.installation.checkStatus() == True):
            self.finishButton.set_opacity(1)
            self.finishButton.set_sensitive(True)
            self.spinner1.stop()
            self.installLabel.set_text(tr('Installation Finished'))
        else: self.installStatus()

    def hideMessage(self, widget):
        self.message.hide()

    def showOrHideAdvOpt(self, widget):
        if self.revadvoptions.get_reveal_child() == True:
            self.revadvoptions.set_reveal_child(False)
        else: self.revadvoptions.set_reveal_child(True)

    def insertCode(self, widget):
        if self.codebox.get_text_length() == 8:
            self.codeToSearch = self.dataConnect.getDataSearch('company_keys', 'companykey', self.codebox.get_text(), "*")
            if self.codeToSearch:
                self.companyId = self.codeToSearch[0][3]
                search = self.dataConnect.getData('company', self.companyId, "name")
                search = search[0][0]
                self.companyName = search
                self.messagebar.set_text(tr("Code for company: ") + "{}".format(self.companyName))
                print (tr("Code for company: ")) + "{}".format(self.companyName)
                self.initial.set_sensitive(True)
            else:
                self.messagebar.set_text(tr("Invalid Code"))
        else: 
            self.initial.set_sensitive(False)
            self.messagebar.set_text("")

    def initialClick(self, widget):
        if self.companyName == "OpenCode":
            self.userCodeFlag = False
            self.initialwindow.hide()
            self.window.show_all()
            self.actualWindowPos = 1
        else:
            self.installation.setInstallPath(self.installation.getInstallPath(), self.companyName) #Por que llamas a este de nuevo? 
            self.userCodeFlag = True
            if self.codeToSearch[0][1]:
                self.inputSVNUser.set_text(self.codeToSearch[0][1])
            if self.codeToSearch[0][2]:
                self.inputSVNPassword.set_text(self.codeToSearch[0][2])
            self.installation.initialization(self.companyId) #Needed, because this initialization starts when you switch to window1
            self.actualWindowPos = 2 #defined in two because, 'startInstall' make 'nextWindow' if SVN credentials are valid
            if self.advoptions.get_active() == True:
                self.workWithAdvancedOptions(widget)
            else: #this is the behavior standard if not selected advanced options
                if self.userCodeFlag: 
                    self.messagebar.set_text(tr("Checking Username and Password from SVN"))
                    self.startInstall(widget)
                else:
                    self.window.show_all()

    """Initializate all values of advanced options by default"""
    def advOptInitial(self):
        self.opt1install.set_active(False) #Select install path
        self.opt2svn.set_active(False) #input svn credentials
        self.opt3report.set_active(False) #show report after installation
        self.opt3report.set_sensitive(False) #TEMPORARY WHILE DON'T WORK
        self.opt4shortcut.set_active(True) #create shortcut after install, only windows.
        self.opt5console.set_active(False)
        self.opt6companyname.set_active(True) #By Default, the last folder must be the company name

    def workWithAdvancedOptions(self, widget):
        shouldStartInstall = True
        if self.opt1install.get_active() or self.opt2svn.get_active(): #Select install path
            self.actualWindowPos = 2
            if self.opt1install.get_active() == False:
                self.folderChooser.set_sensitive(False)
            else:
                self.folderChooser.set_sensitive(True)
            self.preparateWin1()
            self.window1.show_all()
            self.initialwindow.hide()
            shouldStartInstall = False

        if not self.opt2svn.get_active():#input svn credentials
            self.inputSVNUser.set_sensitive(False)
            self.inputSVNPassword.set_sensitive(False)
        else:
            self.inputSVNUser.set_sensitive(True)
            self.inputSVNPassword.set_sensitive(True)

        if self.opt3report.get_active(): #show report after installation
            pass #build it in the future not long away.

        if self.opt4shortcut.get_active(): #create shortcut after install, only windows.
            self.installation.createShortcut = True
            if self.opt5console.get_active(): #create shortcut with --console
                self.installation.openConsole = True
            else:
                self.installation.openConsole = False
        else:
            self.installation.createShortcut = False

        if self.opt6companyname.get_active():
            self.installation.disableLastFolderAsCompanyName = False
        else:
            self.installation.disableLastFolderAsCompanyName = True
            
        if shouldStartInstall:
            self.messagebar.set_text(tr("Checking Username and Password from SVN"))
            self.startInstall(widget)

    def shortcutButtonToggled(self, widget):
        if self.opt4shortcut.get_active():
            self.opt5console.set_sensitive(True)
        else:
            self.opt5console.set_active(False)
            self.opt5console.set_sensitive(False)
