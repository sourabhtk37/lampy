from gi.repository import Gtk
from collections import OrderedDict
from glamp.common.sites import Sites

# @todo separate events class, connect through builder

class SitesTab(Gtk.Box):
     
    def __new__(cls, main_window):
        sites_tab_container = main_window.builder.get_object("sites_tab_container")
        sites_tab_container.__class__ = cls
        return sites_tab_container
    
    def __init__(self, main_window):
        # Gtk.ApplicationWindow.__init__(self)
        # super(MainWindow, self).__init__()

        self.main_window = main_window

        self.sites_list_view = self.main_window.builder.get_object("sites_list_view")
        self.sites_edit_view = self.main_window.builder.get_object("sites_edit_view")

        self.sites_list_container = self.main_window.builder.get_object("sites_list_container")
        self.sites_edit_container = self.main_window.builder.get_object("sites_edit_container")
        self.sites_conf_container = self.main_window.builder.get_object("sites_conf_container")

        self.sites_list_nav = self.main_window.builder.get_object("sites_list_nav")

        self.sites_list_nav_activated = None

        self.sites = Sites().read()

        # edit_button_undo = Gtk.Button(stock=Gtk.STOCK_UNDO)
        edit_button_remove = Gtk.Button(stock=Gtk.STOCK_REMOVE)
        edit_button_add = Gtk.Button(stock=Gtk.STOCK_ADD)
        edit_button_save = Gtk.Button(stock=Gtk.STOCK_SAVE)

        list_button_remove = Gtk.Button(stock=Gtk.STOCK_REMOVE)
        list_button_add = Gtk.Button(stock=Gtk.STOCK_ADD)
        list_button_save = Gtk.Button(stock=Gtk.STOCK_SAVE)

        edit_button_remove.connect('clicked', self.on_edit_remove_clicked)
        edit_button_add.connect('clicked', self.on_edit_add_clicked)
        edit_button_save.connect('clicked', self.on_edit_save_clicked)

        list_button_remove.connect('clicked', self.on_list_remove_clicked)
        list_button_add.connect('clicked', self.on_list_add_clicked)
        list_button_save.connect('clicked', self.on_list_save_clicked)

        self.edit_action_bar = Gtk.ActionBar()
        self.edit_action_bar.add(edit_button_remove)
        self.edit_action_bar.add(edit_button_add)
        self.edit_action_bar.add(edit_button_save)

        self.list_action_bar = Gtk.ActionBar()
        self.list_action_bar.add(list_button_remove)
        self.list_action_bar.add(list_button_add)
        self.list_action_bar.add(list_button_save)

        self.sites_edit_container.add(self.edit_action_bar)
        self.sites_list_container.add(self.list_action_bar)

        self.conf_model = Gtk.ListStore(str, str)
        self.conf_tree = self.main_window.builder.get_object("sites_conf_tree")

        self.build_list_nav()
        self.build_conf_tree()

    def build_list_nav(self):
        for site in self.sites:
            row = Gtk.ListBoxRow()
            if 'ServerName' in site:
                row.add(Gtk.Label(site['ServerName']))
            self.sites_list_nav.add(row)
        self.sites_list_nav.connect('row-activated', self.on_list_nav_activated)

    def rebuild_list_nav(self):
        pass

    def build_conf_tree(self):
        self.conf_tree.set_model(self.conf_model)
        self.conf_tree.set_reorderable(True)
        cols = ['Directive', 'Value']
        for index, title in enumerate(cols):
            cell = Gtk.CellRendererText()
            cell.set_property('editable', True)
            cell.connect('edited', self.on_edit_cell_edited, index)
            col = Gtk.TreeViewColumn(title, cell)
            col.add_attribute(cell, 'text', index)
            self.conf_tree.append_column(col)

    def load_conf_tree(self, id):
        self.conf_model.clear()
        for name, value in self.sites[id].iteritems():
            self.conf_tree_add(name, value)

    def conf_tree_add(self, name=None, value=None):
        self.conf_model.append([name, value])
        self.conf_tree.show_all()

    def on_edit_add_clicked(self, button):
        self.conf_tree_add('', '')

    def on_edit_remove_clicked(self, button):
        list_store, tree_iter = self.conf_tree.get_selection().get_selected()
        if tree_iter:
            list_store.remove(tree_iter)
        self.main_window.resize(1, 1)

    def on_edit_save_clicked(self, button):
        directives = OrderedDict()
        for directive in self.conf_model:
            directives.update({directive[0]: directive[1]})
        self.sites[self.sites_list_nav_activated] = directives
        Sites().write(self.sites)
        self.rebuild_list_nav()

    def on_edit_cell_edited(self, cell, path, text, col):
        self.conf_model[path][col] = text

    def on_list_nav_activated(self, box, row, user_data=None):
        self.sites_list_nav_activated = row.get_index()
        self.load_conf_tree(self.sites_list_nav_activated)
        self.sites_edit_view.show()

    def on_list_add_clicked(self, button):
        self.sites.append({'ServerName': 'server.local', 'DocumentRoot': ''})
        row = Gtk.ListBoxRow()
        row.add(Gtk.Label('server.local'))
        self.sites_list_nav.add(row)
        self.sites_list_nav.show_all()

    def on_list_remove_clicked(self, button):
        self.sites.pop(self.sites_list_nav_activated)
        self.sites_list_nav.remove(self.sites_list_nav.get_selected_row())
        self.main_window.resize(1, 1)

    def on_list_save_clicked(self, button):
        Sites().write(self.sites)
