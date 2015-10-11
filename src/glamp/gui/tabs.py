from gi.repository import Gtk
from collections import OrderedDict
from glamp.lib.storage import Sites

class SitesTab(Gtk.Box):
     
    def __new__(cls, main_window):
        sites_tab_container = main_window.builder.get_object("sites_tab_container")
        sites_tab_container.__class__ = cls
        return sites_tab_container
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.storage = Sites()
        self.sites = self.storage.read()

        self.sites_list_view = self.main_window.builder.get_object("sites_list_view")
        self.sites_edit_view = self.main_window.builder.get_object("sites_edit_view")

        self.sites_list_container = self.main_window.builder.get_object("sites_list_container")
        self.sites_edit_container = self.main_window.builder.get_object("sites_edit_container")
        self.sites_conf_container = self.main_window.builder.get_object("sites_conf_container")

        self.sites_list_nav = self.main_window.builder.get_object("sites_list_nav")
        self.sites_list_nav.connect('row-activated', self.on_list_nav_activated)

        self.conf_tree = self.main_window.builder.get_object("sites_conf_tree")
        self.conf_model = Gtk.ListStore(str, str)
        
        self.edit_hostname_input = self.main_window.builder.get_object("hostname_input")
        self.edit_address_input = self.main_window.builder.get_object("address_input")
        self.edit_docroot_input = self.main_window.builder.get_object("docroot_input")

        self.edit_action_bar = Gtk.ActionBar()
        self.list_action_bar = Gtk.ActionBar()

        self.build_list_nav()
        self.build_conf_tree()
        self.build_list_action_bar()
        self.build_edit_action_bar()

    def build_list_action_bar(self):
        list_button_remove = Gtk.Button(stock=Gtk.STOCK_REMOVE)
        list_button_add = Gtk.Button(stock=Gtk.STOCK_ADD)
        list_button_save = Gtk.Button(stock=Gtk.STOCK_SAVE)

        list_button_remove.connect('clicked', self.on_list_remove_clicked)
        list_button_add.connect('clicked', self.on_list_add_clicked)
        list_button_save.connect('clicked', self.on_list_save_clicked)

        self.list_action_bar.add(list_button_remove)
        self.list_action_bar.add(list_button_add)
        self.list_action_bar.add(list_button_save)
        self.sites_list_container.add(self.list_action_bar)

    def build_edit_action_bar(self):
        edit_button_remove = Gtk.Button(stock=Gtk.STOCK_REMOVE)
        edit_button_add = Gtk.Button(stock=Gtk.STOCK_ADD)
        edit_button_save = Gtk.Button(stock=Gtk.STOCK_SAVE)

        edit_button_remove.connect('clicked', self.on_edit_remove_clicked)
        edit_button_add.connect('clicked', self.on_edit_add_clicked)
        edit_button_save.connect('clicked', self.on_edit_save_clicked)

        self.edit_action_bar.add(edit_button_remove)
        self.edit_action_bar.add(edit_button_add)
        self.edit_action_bar.add(edit_button_save)
        self.sites_edit_container.add(self.edit_action_bar)

    def build_list_nav(self):
        for site in self.sites:
            self.list_nav_add(site)

    def rebuild_list_nav(self):
        pass

    def list_nav_add(self, site):
        row = Gtk.ListBoxRow()
        col = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        col.add(Gtk.Label(site['hostname']))
        col.add(Gtk.Switch())
        row.add(col)
        self.sites_list_nav.add(row)
        self.sites_list_nav.show_all()

    def build_conf_tree(self):
        self.conf_tree.set_model(self.conf_model)
        self.conf_tree.set_reorderable(True)
        for index, title in enumerate(['Property', 'Argument']):
            cell = Gtk.CellRendererText(editable=True)
            cell.connect('edited', self.on_edit_cell_edited, index)
            col = Gtk.TreeViewColumn(title, cell, text=index)
            self.conf_tree.append_column(col)

    def load_conf_tree(self, id):
        self.edit_hostname_input.set_text(self.sites[id]['hostname'])
        self.edit_address_input.set_text(self.sites[id]['address'])
        self.edit_docroot_input.set_filename(self.sites[id]['docroot'])
        self.conf_model.clear()
        for property, argument in self.sites[id]['directives'].iteritems():
            self.conf_tree_add(property, argument)

    def conf_tree_add(self, property=None, argument=None):
        self.conf_model.append([property, argument])
        self.conf_tree.show_all()

    def on_edit_add_clicked(self, button):
        self.conf_tree_add("", "")

    def on_edit_remove_clicked(self, button):
        list_store, tree_iter = self.conf_tree.get_selection().get_selected()
        if tree_iter:
            list_store.remove(tree_iter)
        self.main_window.resize(1, 1)

    def on_edit_save_clicked(self, button):
        id = self.sites_list_nav.get_selected_row().get_index()
        directives = OrderedDict()
        for directive in self.conf_model:
            directives.update({directive[0]: directive[1]})
        self.sites[id]['hostname'] = self.edit_hostname_input.get_text()
        self.sites[id]['address'] = self.edit_address_input.get_text()
        self.sites[id]['docroot'] = self.edit_docroot_input.get_filename()
        self.sites[id]['directives'] = directives
        self.storage.write(self.sites)
        self.rebuild_list_nav()

    def on_edit_cell_edited(self, cell, path, text, col):
        self.conf_model[path][col] = text

    def on_list_nav_activated(self, box, row, user_data=None):
        self.load_conf_tree(row.get_index())
        self.sites_edit_view.show()

    def on_list_add_clicked(self, button):
        site = {
            'hostname': 'virtual.localhost',
            'address': '127.0.0.1',
            'docroot': '',
            'directives': {},
        }
        self.sites.append(site)
        self.list_nav_add(site)

    def on_list_remove_clicked(self, button):
        row = self.sites_list_nav.get_selected_row()
        self.sites.pop(row.get_index())
        self.sites_list_nav.remove(row)
        self.main_window.resize(1, 1)

    def on_list_save_clicked(self, button):
        self.storage.write(self.sites)
