class Server:
    def __init__(self, server, directives=[]):
        self.server = server
        self.directives = directives


class Directive:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Config:
    def __init__(self, server, folder):
        self.server = server
        self.folder = folder
        self.config_file = config_file(server)

    def save(self, directives=[]):
        print ('save')

    def open(self):
        print ('open')


def config_file(server):
    return server
