import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import dataConnection

class firstWindow(Gtk.Window):
    """desc"""
    dataConnect = None

    def __init__(self):
        self.dataConnect = dataConnection.dataConnection()
        self.dataConnect.testConnection()
        builder = Gtk.Builder()
        builder.add_from_file("./GUI/OrangeInstallerGUI.glade")
        handlers = {
            "delete-event": self.userExit,
            "userExit": self.userExit,
            "nextWindow1": self.nextWindow,
            "searching": self.search,
        }
        builder.connect_signals(handlers)
        win = builder.get_object("window1")
        win.show_all()
		
    def userExit(self, widget):
        print("Test")
        exit()

    def nextWindow(self, widget):
        print("Test2")

    def search(self, widget):
        imputTest = widget.get_text()
        print(imputTest)
        resultOfSearch = self.dataConnect.getDataSearch('company','name',imputTest)

        if (len(resultOfSearch) == 0):
            print ('Company not Found, try again')
        if (len(resultOfSearch) > 1):
            print ("Too many result, select one if it's here")
            for i in range(len(resultOfSearch)):
                if (i > 9):
                    print ("Some result not shown in screen. Choose '666' to search again")
                    break
                print('{}: {}'.format(i, resultOfSearch[i][1]))