from gi.repository import Gtk

from lampy.controllers.tabs import SitesTab


class MainWindow(object):
    def __init__(self, application):

        self.builder = application.builder
        self.builder.add_from_file("lampy/layouts/main_window.xml")

        self.layout = self.builder.get_object("main_window")  # Gtk.ApplicationWindow
        self.layout.connect('delete-event', Gtk.main_quit)

        self.sites_tab_container = SitesTab(self)

        self.layout.show_all()
        self.sites_tab_container.edit_view.hide()
