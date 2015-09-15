# @todo porting the gui to Glade and Gtk.Builder

from gi.repository import Gtk
from collections import OrderedDict

from glampy.common.sites import Sites
from glampy.gui.conf import Conf


class Main(Gtk.Window):
    def __init__(self):
        super(Main, self).__init__()

        self.gtk_layout = Gtk.VBox()
        self.gtk_system = Gtk.VBox()
        self.gtk_templates = Gtk.VBox()
        self.gtk_tabs = Gtk.Notebook()
        self.gtk_main_controls = Gtk.HButtonBox()

        self.sites = Sites().read()

        self.gtk_sites_table = {}

        self.build_main_controls()
        self.build_sites_table()
        self.build_layout()
        self.build_system()
        self.build_tabs()

        self.add(self.gtk_tabs)

        self.set_title('Glampy')
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect('destroy', Gtk.main_quit)

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
            'controls': OrderedDict([
                ('remove', []),
                ('server', []),
                ('folder', []),
                ('config', []),
                ('enable', []),
            ])
        }
        for site in self.sites:
            self.sites_table_add(site)

    def reset_sites_table(self):
        self.sites = Sites().read()
        self.gtk_sites_table['container'].destroy()
        self.build_sites_table()
        self.gtk_layout.add(self.gtk_sites_table['container'])
        self.resize(1, 1)

    def sites_table_add(self, directives={}):
        controls = {
            'server': Gtk.Entry(),
            'folder': Gtk.FileChooserButton('Folder'),
            'config': Gtk.Button(stock=Gtk.STOCK_PROPERTIES),
            'enable': Gtk.Switch(),
            'remove': Gtk.Button(stock=Gtk.STOCK_REMOVE),
        }
        controls['folder'].set_action(Gtk.FileChooserAction.SELECT_FOLDER)

        if 'ServerName' in directives and directives['ServerName']:
            controls['server'].set_text(directives['ServerName'])
        if 'DocumentRoot' in directives and directives['DocumentRoot']:
            controls['folder'].set_current_folder(directives['DocumentRoot'])

        controls['config'].connect('clicked', self.on_config_clicked)
        controls['remove'].connect('clicked', self.on_remove_clicked)
        # controls['enable'].connect('clicked', self.on_enable_clicked)

        child = Gtk.HBox()

        for control in self.gtk_sites_table['controls']:
            self.gtk_sites_table['controls'][control].append(controls[control])
            child.add(self.gtk_sites_table['controls'][control][-1])

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
        self.sites[index].update({'ServerName': server, 'DocumentRoot': folder})
        Conf(self, index)

    def on_enable_clicked(self, button):
        pass

    def on_remove_clicked(self, button):
        index = self.gtk_sites_table['controls']['remove'].index(button)
        self.sites.pop(index)
        self.sites_table_remove(index)

    def on_add_clicked(self, button):
        self.sites.append({'ServerName': '', 'DocumentRoot': ''})
        self.sites_table_add()

    def on_reset_clicked(self, button):
        self.reset_sites_table()

    def on_save_clicked(self, button):
        for index, site in enumerate(self.sites):
            server = self.gtk_sites_table['controls']['server'][index].get_text()
            folder = self.gtk_sites_table['controls']['folder'][index].get_current_folder()
            site.update({'DocumentRoot': folder, 'ServerName': server})
        Sites().write(self.sites)
        self.reset_sites_table()
