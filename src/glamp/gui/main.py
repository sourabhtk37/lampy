from collections import OrderedDict
from gi.repository import Gtk

from glamp.common.sites import Sites

# @todo separate events class

class Main(object):
    def __init__(self):

        self.gtk_builder = Gtk.Builder()

        self.ui_layout = self.gtk_builder.new_from_file("glamp/gui/glade/main_window.glade")
        self.ui_sites_list_container = self.gtk_builder.new_from_file("glamp/gui/glade/sites_list_container.glade")
        self.ui_sites_edit_container = self.gtk_builder.new_from_file("glamp/gui/glade/sites_edit_container.glade")

        self.gtk_main_window = self.ui_layout.get_object("main_window")

        self.gtk_sites_list_view = self.ui_layout.get_object("sites_list_view")
        self.gtk_sites_edit_view = self.ui_layout.get_object("sites_edit_view")

        self.gtk_sites_list_view.add(self.ui_sites_list_container.get_object("sites_list_container"))
        self.gtk_sites_edit_view.add(self.ui_sites_edit_container.get_object("sites_edit_container"))

        self.gtk_sites_list_container = self.ui_sites_list_container.get_object("sites_list_container")
        self.gtk_sites_edit_container = self.ui_sites_edit_container.get_object("sites_edit_container")
        self.gtk_sites_conf_container = self.ui_sites_edit_container.get_object("sites_conf_container")

        self.gtk_sites_list_nav = self.ui_sites_list_container.get_object("sites_list_nav")

        self.sites_list_nav_activated = None

        self.sites = Sites().read()

        # gtk_edit_button_undo = Gtk.Button(stock=Gtk.STOCK_UNDO)
        gtk_edit_button_remove = Gtk.Button(stock=Gtk.STOCK_REMOVE)
        gtk_edit_button_add = Gtk.Button(stock=Gtk.STOCK_ADD)
        gtk_edit_button_save = Gtk.Button(stock=Gtk.STOCK_SAVE)

        gtk_list_button_remove = Gtk.Button(stock=Gtk.STOCK_REMOVE)
        gtk_list_button_add = Gtk.Button(stock=Gtk.STOCK_ADD)
        gtk_list_button_save = Gtk.Button(stock=Gtk.STOCK_SAVE)

        gtk_edit_button_remove.connect('clicked', self.on_edit_remove_clicked)
        gtk_edit_button_add.connect('clicked', self.on_edit_add_clicked)
        gtk_edit_button_save.connect('clicked', self.on_edit_save_clicked)

        gtk_list_button_remove.connect('clicked', self.on_list_remove_clicked)
        gtk_list_button_add.connect('clicked', self.on_list_add_clicked)
        gtk_list_button_save.connect('clicked', self.on_list_save_clicked)

        self.gtk_edit_action_bar = Gtk.ActionBar()
        self.gtk_edit_action_bar.add(gtk_edit_button_remove)
        self.gtk_edit_action_bar.add(gtk_edit_button_add)
        self.gtk_edit_action_bar.add(gtk_edit_button_save)

        self.gtk_list_action_bar = Gtk.ActionBar()
        self.gtk_list_action_bar.add(gtk_list_button_remove)
        self.gtk_list_action_bar.add(gtk_list_button_add)
        self.gtk_list_action_bar.add(gtk_list_button_save)

        self.gtk_sites_edit_container.add(self.gtk_edit_action_bar)
        self.gtk_sites_list_container.add(self.gtk_list_action_bar)

        self.gtk_conf_model = Gtk.ListStore(str, str)
        self.gtk_conf_tree = self.ui_sites_edit_container.get_object("sites_conf_tree")

        self.build_list_nav()
        self.build_conf_tree()
        
        self.gtk_main_window.connect("delete-event", Gtk.main_quit)

        self.gtk_main_window.show_all()

        self.gtk_sites_edit_container.hide()

        Gtk.main()

    def build_list_nav(self):
        for site in self.sites:
            row = Gtk.ListBoxRow()
            if 'ServerName' in site:
                row.add(Gtk.Label(site['ServerName']))
            self.gtk_sites_list_nav.add(row)
        self.gtk_sites_list_nav.connect('row-activated', self.on_list_nav_activated)

    def rebuild_list_nav(self):
        pass

    def build_conf_tree(self):
        self.gtk_conf_tree.set_model(self.gtk_conf_model)
        self.gtk_conf_tree.set_reorderable(True)
        cols = ['Directive', 'Value']
        for index, title in enumerate(cols):
            cell = Gtk.CellRendererText()
            cell.set_property('editable', True)
            cell.connect('edited', self.on_edit_cell_edited, index)
            col = Gtk.TreeViewColumn(title, cell)
            col.add_attribute(cell, 'text', index)
            self.gtk_conf_tree.append_column(col)

    def load_conf_tree(self, id):
        self.gtk_conf_model.clear()
        for name, value in self.sites[id].iteritems():
            self.conf_tree_add(name, value)

    def conf_tree_add(self, name=None, value=None):
        self.gtk_conf_model.append([name, value])
        self.gtk_conf_tree.show_all()

    def on_edit_add_clicked(self, button):
        self.conf_tree_add('', '')

    def on_edit_remove_clicked(self, button):
        list_store, tree_iter = self.gtk_conf_tree.get_selection().get_selected()
        if tree_iter:
            list_store.remove(tree_iter)
        self.gtk_main_window.resize(1, 1)

    def on_edit_save_clicked(self, button):
        directives = OrderedDict()
        for directive in self.gtk_conf_model:
            directives.update({directive[0]: directive[1]})
        self.sites[self.sites_list_nav_activated] = directives
        Sites().write(self.sites)
        self.rebuild_list_nav()

    def on_edit_cell_edited(self, cell, path, text, col):
        self.gtk_conf_model[path][col] = text

    def on_list_nav_activated(self, box, row, user_data=None):
        self.sites_list_nav_activated = row.get_index()
        self.load_conf_tree(self.sites_list_nav_activated)
        self.gtk_sites_edit_container.show()

    def on_list_add_clicked(self, button):
        self.sites.append({'ServerName': 'server.local', 'DocumentRoot': ''})
        row = Gtk.ListBoxRow()
        row.add(Gtk.Label('server.local'))
        self.gtk_sites_list_nav.add(row)
        self.gtk_sites_list_nav.show_all()

    def on_list_remove_clicked(self, button):
        self.sites.pop(self.sites_list_nav_activated)
        self.gtk_sites_list_nav.remove(self.gtk_sites_list_nav.get_selected_row())
        self.gtk_main_window.resize(1, 1)

    def on_list_save_clicked(self, button):
        Sites().write(self.sites)
