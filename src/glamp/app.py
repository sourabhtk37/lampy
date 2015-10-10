from gi.repository import Gtk, Gio
from glamp.gui import window

class Application(Gtk.Application):

    def __init__(self):
        # Gtk.Application.__init__(self)
        super(Application, self).__init__()

        self.builder = Gtk.Builder()
        self.builder.add_from_file("glamp/gui/ui/main_window.xml")

        self.connect('activate', self.on_activate)
        
    def on_activate(self, data=None):
        main_window = window.MainWindow(self)

# if __name__ == '__main__':
#     app.Application().run()
#     Gtk.main()