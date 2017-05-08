import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from window import firstWindow
import dataConnection

class mainGUI(object):
    """Main GUI controller"""

    def __init__(self, **kwargs):
        firstWindow()
        Gtk.main()