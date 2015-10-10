from gi.repository import Gtk
from collections import OrderedDict
from glamp.gui.tab import SitesTab

class MainWindow(Gtk.ApplicationWindow):
     
    def __new__(cls, application):
        application.builder.add_from_file("glamp/gui/ui/main_window.xml")
        main_window = application.builder.get_object("main_window")
        main_window.__class__ = cls
        return main_window
    
    def __init__(self, application):
        # super(MainWindow, self).__init__()
        self.connect('delete-event', Gtk.main_quit)

        self.builder = application.builder
        self.sites_tab_container = SitesTab(self)

        self.show_all()
        self.sites_tab_container.sites_edit_view.hide()
