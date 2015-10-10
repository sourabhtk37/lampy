from gi.repository import Gtk
from collections import OrderedDict
from glamp.gui.tab import SitesTab

# @todo separate events class

class MainWindow(Gtk.ApplicationWindow):
     
    def __new__(cls, application):
        main_window = application.builder.get_object("main_window")
        main_window.__class__ = cls
        return main_window
    
    def __init__(self, application):
        # Gtk.ApplicationWindow.__init__(self)
        # super(MainWindow, self).__init__()

        self.builder = application.builder

        self.sites_tab_container = SitesTab(self)
        
        self.connect('delete-event', Gtk.main_quit)

        self.show_all()
        self.sites_tab_container.sites_edit_view.hide()
