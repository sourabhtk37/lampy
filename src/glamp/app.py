from gi.repository import Gtk, Gio
from glamp.gui import window

class Application(Gtk.Application):

    def __init__(self):
        super(Application, self).__init__()

        self.connect('activate', self.on_activate)

        self.builder = Gtk.Builder()

    def on_activate(self, data=None):
        main_window = window.MainWindow(self)
