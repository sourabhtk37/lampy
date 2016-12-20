from gi.repository import Gtk

from glamp.controllers.tabs import SitesTab


class MainWindow(Gtk.ApplicationWindow):
    def __new__(cls, application):
        application.builder.add_from_file("glamp/layouts/main_window.xml")
        self = application.builder.get_object("main_window")
        self.__class__ = cls
        return self

    def __init__(self, application):
        self.connect('delete-event', Gtk.main_quit)

        self.builder = application.builder
        self.sites_tab_container = SitesTab(self)

        self.show_all()
        self.sites_tab_container.edit_view.hide()
