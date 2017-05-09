import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import dataConnection

class firstWindow(Gtk.Window):
    """desc"""
    dataConnect = None

    def __init__(self):
        self.dataConnect = dataConnection.dataConnection()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./GUI/OrangeInstallerGUI.glade")
        self.handlers = {
            "delete-event": self.userExit,
            "userExit": self.userExit,
            "nextWindow1": self.nextWindow,
            "searching": self.search,
        }
        self.builder.connect_signals(self.handlers)
        self.win = self.builder.get_object("window1")
        self.win.show_all()
        #load objects for working.
        self.liststore = self.builder.get_object('liststore')
        self.listview = self.builder.get_object('treeview')
        self.statusbar = self.builder.get_object('statusbar')
        #check database Status
        dbcheck = self.dataConnect.testConnection()
        if dbcheck:
            self.communicator('Success connecting to database')
        else: self.communicator('Fail to connect with database')
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Company", renderer, text=0)
        self.listview.append_column(column)
		
    def userExit(self, widget):
        print("Test")
        exit()

    def nextWindow(self, widget):
        print("Test2")
    
    def communicator(self, message):
        self.statusbar.push(1,message)

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
        