# @todo porting the gui to Glade and Gtk.Builder

from gi.repository import Gtk
from collections import OrderedDict

import common.config


class Main(Gtk.Window):
    def __init__(self):
        # super(Main, self).__init__(Gtk.WINDOW_TOPLEVEL)
        super(Main, self).__init__()

        self.set_title('Glampy')

        # self.set_position(Gtk.WIN_POS_CENTER)
        self.connect('destroy', Gtk.main_quit)

        self.gtk_layout = Gtk.VBox()
        self.gtk_system = Gtk.VBox()
        self.gtk_templates = Gtk.VBox()
        self.gtk_tabs = Gtk.Notebook()
        self.gtk_main_controls = Gtk.HButtonBox()

        self.site_list = common.config.Config().read()

        self.gtk_sites_table = {}

        self.build_main_controls()
        self.build_sites_table()
        self.build_layout()
        self.build_system()
        self.build_tabs()

        self.add(self.gtk_tabs)

        self.show_all()
        self.resize(1, 1)

        Gtk.main()

    def build_layout(self):
        self.gtk_layout.add(self.gtk_main_controls)
        self.gtk_layout.add(self.gtk_sites_table['container'])

    def build_system(self):
        pass

    def build_tabs(self):
        sites_tab = Gtk.Label()
        system_tab = Gtk.Label()
        templates_tab = Gtk.Label()

        sites_tab.set_text('Sites')
        system_tab.set_text('System')
        templates_tab.set_text('Templates')

        self.gtk_tabs.append_page(self.gtk_layout, sites_tab)
        self.gtk_tabs.append_page(self.gtk_system, system_tab)
        self.gtk_tabs.append_page(self.gtk_templates, templates_tab)

    def build_main_controls(self):
        add_control = Gtk.Button(stock=Gtk.STOCK_ADD)
        reset_control = Gtk.Button(stock=Gtk.STOCK_UNDO)
        save_control = Gtk.Button(stock=Gtk.STOCK_SAVE)

        add_control.connect('clicked', self.on_add_clicked)
        reset_control.connect('clicked', self.on_reset_clicked)
        save_control.connect('clicked', self.on_save_clicked)

        self.gtk_main_controls.add(add_control)
        self.gtk_main_controls.add(reset_control)
        self.gtk_main_controls.add(save_control)

    def build_sites_table(self):
        self.gtk_sites_table = {
            'container': Gtk.VBox(),
            'children': [],
            'controls': {
                'server': [],
                'folder': [],
                'config': [],
                'remove': [],
                'enable': [],
            }
        }
        for site in self.site_list:
            self.sites_table_add(site)

    def reset_sites_table(self):
        self.site_list = common.config.Config().read()
        self.gtk_sites_table['container'].destroy()
        self.build_sites_table()
        self.gtk_layout.add(self.gtk_sites_table['container'])
        self.resize(1, 1)

    def sites_table_add(self, directives={}):
        controls = {
            'server': Gtk.Entry(),
            'folder': Gtk.FileChooserButton('Folder'),
            'config': Gtk.Button(stock=Gtk.STOCK_PROPERTIES),
            'remove': Gtk.Button(stock=Gtk.STOCK_REMOVE),
            'enable': Gtk.Button(stock=Gtk.STOCK_CONNECT),
        }
        # controls['folder'].set_action(Gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)

        if 'ServerName' in directives and directives['ServerName']:
            controls['server'].set_text(directives['ServerName'])
        if 'DocumentRoot' in directives and directives['DocumentRoot']:
            controls['folder'].set_current_folder(directives['DocumentRoot'])

        controls['config'].connect('clicked', self.on_config_clicked)
        controls['remove'].connect('clicked', self.on_remove_clicked)
        controls['enable'].connect('clicked', self.on_enable_clicked)

        for control in self.gtk_sites_table['controls']:
            self.gtk_sites_table['controls'][control].append(controls[control])

        child = Gtk.HBox()
        child.add(self.gtk_sites_table['controls']['remove'][-1])
        child.add(self.gtk_sites_table['controls']['server'][-1])
        child.add(self.gtk_sites_table['controls']['folder'][-1])
        child.add(self.gtk_sites_table['controls']['config'][-1])
        child.add(self.gtk_sites_table['controls']['enable'][-1])

        self.gtk_sites_table['children'].append(child)

        self.gtk_sites_table['container'].add(self.gtk_sites_table['children'][-1])
        self.gtk_sites_table['container'].show_all()

    def sites_table_remove(self, index):
        self.gtk_sites_table['container'].remove(self.gtk_sites_table['children'][index])
        self.gtk_sites_table['children'][index].destroy()
        self.gtk_sites_table['container'].check_resize()
        self.resize(1, 1)

        for control in self.gtk_sites_table['controls']:
            del self.gtk_sites_table['controls'][control][index]
        del self.gtk_sites_table['children'][index]

    def on_config_clicked(self, button):
        index = self.gtk_sites_table['controls']['config'].index(button)
        server = self.gtk_sites_table['controls']['server'][index].get_text()
        folder = self.gtk_sites_table['controls']['folder'][index].get_current_folder()
        self.site_list[index].update({'ServerName': server, 'DocumentRoot': folder})
        Config(self, index)

    def on_enable_clicked(self, button):
        pass

    def on_remove_clicked(self, button):
        index = self.gtk_sites_table['controls']['remove'].index(button)
        self.site_list.pop(index)
        self.sites_table_remove(index)

    def on_add_clicked(self, button):
        self.site_list.append({'ServerName': '', 'DocumentRoot': ''})
        self.sites_table_add()

    def on_reset_clicked(self, button):
        self.reset_sites_table()

    def on_save_clicked(self, button):
        for index, site in enumerate(self.site_list):
            server = self.gtk_sites_table['controls']['server'][index].get_text()
            folder = self.gtk_sites_table['controls']['folder'][index].get_current_folder()
            site.update({'DocumentRoot': folder, 'ServerName': server})
        common.config.Config().write(self.site_list)
        self.reset_sites_table()


class Config(Gtk.Window):
    def __init__(self, main_window, index):
        # super(Config, self).__init__(Gtk.WINDOW_TOPLEVEL)
        super(Config, self).__init__()

        self.main_window = main_window
        self.site_list = main_window.site_list

        self.index = index
        self.server = self.site_list[index]['ServerName']
        self.folder = self.site_list[index]['DocumentRoot']

        # self.set_position(Gtk.WIN_POS_CENTER)
        self.set_modal(True)
        self.set_title(self.server)

        self.gtk_layout = Gtk.VBox()
        self.gtk_main_controls = Gtk.HButtonBox()
        self.gtk_config_model = Gtk.ListStore(str, str)
        self.gtk_config_tree = Gtk.TreeView()

        self.build_main_controls()
        self.build_config_tree()
        self.build_layout()

        self.add(self.gtk_layout)

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

        for name, value in self.site_list[self.index].iteritems():
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
        self.site_list[self.index] = directives
        common.config.Config().write(self.site_list)
        self.main_window.reset_sites_table()

    def on_cell_edited(self, cell, path, text, col):
        self.gtk_config_model[path][col] = text
