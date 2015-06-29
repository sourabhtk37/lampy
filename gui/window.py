import gtk
import common.config


class Main(gtk.Window):
    def __init__(self):
        super(Main, self).__init__(gtk.WINDOW_TOPLEVEL)

        self.set_position(gtk.WIN_POS_CENTER)
        self.connect('destroy', gtk.main_quit)
        self.set_title('Glamp')

        self.gtk_layout = gtk.VBox()
        self.gtk_tabs = gtk.Notebook()
        self.gtk_main_controls = gtk.HButtonBox()

        self.gtk_sites_table = {
            'container': gtk.VBox(),
            'children': [],
            'controls': {
                'server': [],
                'folder': [],
                'config': [],
                'remove': [],
                'enable': [],
            }
        }

        self.build_main_controls()
        self.build_sites_table()
        self.build_layout()
        self.build_tabs()

        self.add(self.gtk_tabs)

        self.show_all()
        self.resize(1, 1)

    def build_layout(self):
        self.gtk_layout.add(self.gtk_main_controls)
        self.gtk_layout.add(self.gtk_sites_table['container'])

    def build_tabs(self):
        first_tab = gtk.Label()
        first_tab.set_text('Virtual Hosts')
        self.gtk_tabs.append_page(self.gtk_layout, first_tab)

    def build_main_controls(self):
        add_control = gtk.Button('Add')
        save_control = gtk.Button('Save')

        add_control.connect('clicked', self.on_add_clicked)
        save_control.connect('clicked', self.on_save_clicked)

        self.gtk_main_controls.add(add_control)
        self.gtk_main_controls.add(save_control)

    def build_sites_table(self):
        sites = common.config.Config().open()
        for site in sites:
            self.sites_table_add(site)

    def sites_table_add(self, directives={}):
        controls = {
            'server': gtk.Entry(),
            'folder': gtk.FileChooserButton('Folder'),
            'config': gtk.Button('Config'),
            'remove': gtk.Button('Remove'),
            'enable': gtk.Button('Enable'),
        }
        controls['folder'].set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)

        if 'ServerName' in directives and directives['ServerName']:
            controls['server'].set_text(directives['ServerName'])
        if 'DocumentRoot' in directives and directives['DocumentRoot']:
            controls['folder'].set_current_folder(directives['DocumentRoot'])

        controls['config'].connect('clicked', self.on_config_clicked)
        controls['remove'].connect('clicked', self.on_remove_clicked)
        controls['enable'].connect('clicked', self.on_enable_clicked)

        for control in self.gtk_sites_table['controls']:
            self.gtk_sites_table['controls'][control].append(controls[control])

        child = gtk.HBox()
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
        Config(index, server, folder)

    def on_enable_clicked(self, button):
        print ('enable')

    def on_remove_clicked(self, button):
        index = self.gtk_sites_table['controls']['remove'].index(button)
        self.sites_table_remove(index)

    def on_add_clicked(self, button):
        self.sites_table_add()

    def on_save_clicked(self, button):
        print ('save')

    def main(self):
        gtk.main()


class Config(gtk.Window):
    def __init__(self, index, server, folder):
        super(Config, self).__init__(gtk.WINDOW_TOPLEVEL)

        self.set_position(gtk.WIN_POS_CENTER)
        self.set_modal(True)
        self.set_title(server)

        self.index = index
        self.server = server
        self.folder = folder

        self.gtk_layout = gtk.VBox()
        self.gtk_main_controls = gtk.HButtonBox()
        self.gtk_config_model = gtk.ListStore(str, str)
        self.gtk_config_tree = gtk.TreeView(model=self.gtk_config_model)

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
        add_control = gtk.Button('Add')
        save_control = gtk.Button('Save')

        add_control.connect('clicked', self.on_add_clicked)
        save_control.connect('clicked', self.on_save_clicked)

        self.gtk_main_controls.add(add_control)
        self.gtk_main_controls.add(save_control)

    def build_config_tree(self):
        cols = ['Directive', 'Value']

        for col, title in enumerate(cols):
            cell = gtk.CellRendererText()
            cell.set_property('editable', True)
            cell.connect('edited', self.on_cell_edited, col)
            self.gtk_config_tree.append_column(gtk.TreeViewColumn(title, cell, text=col))

        sites = common.config.Config().open()

        if self.index < len(sites) and len(sites[self.index]):
            for name, value in sites[self.index].iteritems():
                self.config_tree_add(name, value)
        else:
            self.config_tree_add('ServerName', self.server)
            self.config_tree_add('DocumentRoot', self.folder)

    def config_tree_add(self, name=None, value=None):
        self.gtk_config_model.append([name, value])
        self.gtk_config_tree.show_all()

    def on_add_clicked(self, button):
        self.config_tree_add(None, None)

    def on_save_clicked(self, button):
        config = common.config.Config()
        config.save(self.index, self.gtk_config_model)

    def on_cell_edited(self, cell, path, text, col):
        self.gtk_config_model[path][col] = text
