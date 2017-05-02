import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class firstWindow(Gtk.Window):
    """desc"""
    def __init__(self):
        Gtk.Window.__init__(self, title="OrangeInstaller")

    def on_button_clicked(self, widget):
        pass

