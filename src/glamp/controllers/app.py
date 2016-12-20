from gi.repository import Gtk

from glamp.controllers import window


class Application(Gtk.Application):
    def __init__(self):
        super(Application, self).__init__()

        self.connect('activate', self.on_activate)

        self.builder = Gtk.Builder()

    def on_activate(self, data=None):
        window.MainWindow(self)
        Gtk.main()
