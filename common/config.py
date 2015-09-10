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

    def write(self, content):
        with open(self.config_file, 'w') as f:
            json.dump(content, f)

    def read(self):
        with open(self.config_file, 'r') as f:
            content = f.read()
        if not content:
            return [{}]
        return json.loads(content)

    def update(self, index, directives={}):
        content = self.read()
        count = len(content)

        if index > count:
            # Adding site before saving previous in list
            return
        if index == count:
            content.append(directives)
        else:
            content[index].update(directives)
        self.write(content)

    def remove(self, index=[]):
        if index:
            content = self.read()
            for i in sorted(index, reverse=True):
                if i < len(content):
                    del content[i]
            self.write(content)

def config_file():
    return os.path.expanduser('~') + '/' + APP_DIR + '/sites.json'
