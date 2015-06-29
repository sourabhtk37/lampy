import os
import json
from common import APP_DIR


class Server(object):
    def __init__(self, server, directives=[]):
        self.server = server
        self.directives = directives


class Directive(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Config(object):
    def __init__(self):
        self.config_file = config_file()
        if not os.path.exists(os.path.dirname(self.config_file)):
            os.makedirs(os.path.dirname(self.config_file))

    def save(self, index, directives=[]):
        content = self.open()
        count = len(content)
        dict_directives = {}

        for directive in directives:
            dict_directives[directive[0]] = directive[1]

        if index > count:
            # Adding site before saving previous in list
            # @todo raise exception?
            return

        if index == count:
            content.append(dict_directives)
        else:
            content[index] = dict_directives

        with open(self.config_file, 'w') as f:
            json.dump(content, f)

    def open(self):
        with open(self.config_file, 'r') as f:
            content = f.read()
        if not content:
            return [{}]
        return json.loads(content)


def config_file():
    return os.path.expanduser('~') + '/' + APP_DIR + '/sites.json'
