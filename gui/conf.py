from gi.repository import Gtk
from collections import OrderedDict

from glampy.common.sites import Sites


class Conf(Gtk.Window):
    def __init__(self, main, index):
        super(Conf, self).__init__()

        self.main = main
        self.sites = main.sites

        self.index = index
        self.server = self.sites[index]['ServerName']
        self.folder = self.sites[index]['DocumentRoot']

        self.gtk_layout = Gtk.VBox()
        self.gtk_main_controls = Gtk.HButtonBox()
        self.gtk_config_model = Gtk.ListStore(str, str)
        self.gtk_config_tree = Gtk.TreeView()

        self.build_main_controls()
        self.build_config_tree()
        self.build_layout()

        self.add(self.gtk_layout)

        self.set_modal(True)
        self.set_title(self.server)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.show_all()
        self.resize(1, 1)

    def build_layout(self):
        self.gtk_layout.add(self.gtk_main_controls)
        self.gtk_layout.add(self.gtk_config_tree)

    def build_main_controls(self):
        add_control = Gtk.Button(stock=Gtk.STOCK_ADD)
        remove_control = Gtk.Button(stock=Gtk.STOCK_REMOVE)
        save_control = Gtk.Button(stock=Gtk.STOCK_SAVE)

        add_control.connect('clicked', self.on_add_clicked)
        remove_control.connect('clicked', self.on_remove_clicked)
        save_control.connect('clicked', self.on_save_clicked)

        self.gtk_main_controls.add(add_control)
        self.gtk_main_controls.add(remove_control)
        self.gtk_main_controls.add(save_control)

    def build_config_tree(self):
        self.gtk_config_tree.set_model(self.gtk_config_model)
        self.gtk_config_tree.set_reorderable(True)
        cols = ['Directive', 'Value']
        for index, title in enumerate(cols):
            cell = Gtk.CellRendererText()
            cell.set_property('editable', True)
            cell.connect('edited', self.on_cell_edited, index)
            col = Gtk.TreeViewColumn(title, cell)
            col.add_attribute(cell, 'text', index)
            self.gtk_config_tree.append_column(col)

        for name, value in self.sites[self.index].iteritems():
            self.config_tree_add(name, value)

    def config_tree_add(self, name=None, value=None):
        self.gtk_config_model.append([name, value])
        self.gtk_config_tree.show_all()

    def on_add_clicked(self, button):
        self.config_tree_add('', '')

    def on_remove_clicked(self, button):
        list_store, tree_iter = self.gtk_config_tree.get_selection().get_selected()
        if tree_iter:
            list_store.remove(tree_iter)
        self.resize(1, 1)

    def on_save_clicked(self, button):
        directives = OrderedDict()
        for directive in self.gtk_config_model:
            directives.update({directive[0]: directive[1]})
        self.sites[self.index] = directives
        Sites().write(self.sites)
        self.main.reset_sites_table()

    def on_cell_edited(self, cell, path, text, col):
        self.gtk_config_model[path][col] = text
