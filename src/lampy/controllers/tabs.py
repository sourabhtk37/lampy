from collections import OrderedDict
from gi.repository import Gtk

from lampy.models.storage import Sites


class SitesTab(object):
    def __init__(self, main_window):

        self.main_window = main_window.layout
        self.builder = main_window.builder
        self.layout = self.builder.get_object("sites_tab_container")  # Gtk.Box

        self.storage = Sites()
        self.sites = self.storage.read()
        self.list_active = None

        self.list_view = self.builder.get_object("sites_list_view")
        self.edit_view = self.builder.get_object("sites_edit_view")

        self.list_container = self.builder.get_object("sites_list_container")
        self.edit_container = self.builder.get_object("sites_edit_container")
        self.conf_container = self.builder.get_object("sites_conf_container")

        self.list_nav = self.builder.get_object("sites_list_nav")
        self.conf_tree = self.builder.get_object("sites_conf_tree")
        self.conf_model = Gtk.ListStore(str, str)

        self.edit_hostname_input = self.builder.get_object("hostname_input")
        self.edit_address_input = self.builder.get_object("address_input")
        self.edit_docroot_input = self.builder.get_object("docroot_input")

        self.build_list_nav()
        self.build_conf_tree()
        self.build_list_action_bar()
        self.build_edit_action_bar()

    def build_list_action_bar(self):
        list_remove_button = self.builder.get_object("sites_list_remove_button")
        list_add_button = self.builder.get_object("sites_list_add_button")
        list_save_button = self.builder.get_object("sites_list_save_button")

        list_remove_button.connect('clicked', self.on_list_remove_clicked)
        list_add_button.connect('clicked', self.on_list_add_clicked)
        list_save_button.connect('clicked', self.on_list_save_clicked)

    def build_edit_action_bar(self):
        edit_remove_button = self.builder.get_object("sites_edit_remove_button")
        edit_add_button = self.builder.get_object("sites_edit_add_button")
        edit_save_button = self.builder.get_object("sites_edit_save_button")

        edit_remove_button.connect('clicked', self.on_edit_remove_clicked)
        edit_add_button.connect('clicked', self.on_edit_add_clicked)
        edit_save_button.connect('clicked', self.on_edit_save_clicked)

    def build_list_nav(self):
        for site in self.sites:
            self.list_nav_add(site)
        self.list_nav.connect('row-activated', self.on_list_nav_activated)

    def rebuild_list_nav(self):
        pass

    def list_nav_add(self, site):
        builder = self.builder.new_from_file("lampy/layouts/sites_list_nav_row.xml")
        row = Gtk.ListBoxRow()
        col = builder.get_object("sites_list_nav_row")
        label = builder.get_object("sites_list_nav_row_label")
        switch = builder.get_object("sites_list_nav_row_switch")
        label.set_text(site['hostname'])
        row.add(col)
        self.list_nav.add(row)
        self.list_nav.show_all()

    def build_conf_tree(self):
        self.conf_tree.set_model(self.conf_model)
        for index, title in enumerate(['Property', 'Arguments']):
            cell = Gtk.CellRendererText(editable=True)
            cell.connect('edited', self.on_edit_cell_edited, index)
            col = Gtk.TreeViewColumn(title, cell, text=index)
            self.conf_tree.append_column(col)

    def load_conf_tree(self, id):
        self.edit_hostname_input.set_text(self.sites[id]['hostname'])
        self.edit_address_input.set_text(self.sites[id]['address'])
        self.edit_docroot_input.set_filename(self.sites[id]['docroot'])
        self.conf_model.clear()
        for prop, args in self.sites[id]['directives'].iteritems():
            self.conf_tree_add(prop, args)
        self.main_window.resize(1, 1)

    def conf_tree_add(self, prop=None, args=None):
        self.conf_model.append([prop, args])
        self.conf_tree.show_all()

    def on_edit_add_clicked(self, button):
        self.conf_tree_add("", "")

    def on_edit_remove_clicked(self, button):
        list_store, tree_iter = self.conf_tree.get_selection().get_selected()
        if tree_iter:
            list_store.remove(tree_iter)
            self.main_window.resize(1, 1)

    def on_edit_save_clicked(self, button):
        id = self.list_active.get_index()
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
        self.list_active = row
        self.load_conf_tree(self.list_active.get_index())
        self.edit_view.show()

    def on_list_add_clicked(self, button):
        new = {
            'hostname': "virtual.localhost",
            'address': "127.0.0.1",
            'docroot': "",
            'directives': {},
        }
        self.sites.append(new)
        self.list_nav_add(new)

    def on_list_remove_clicked(self, button):
        if self.list_active:
            self.sites.pop(self.list_active.get_index())
            self.list_nav.remove(self.list_active)
            self.list_active = None
            self.main_window.resize(1, 1)

    def on_list_save_clicked(self, button):
        self.storage.write(self.sites)
