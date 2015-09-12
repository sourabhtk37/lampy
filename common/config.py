import os
import json
from collections import OrderedDict

from common import APP_DIR


class Config(object):
    def __init__(self):
        self.config_file = config_file()
        if not os.path.exists(os.path.dirname(self.config_file)):
            os.makedirs(os.path.dirname(self.config_file))

    def read(self):
        with open(self.config_file, 'r') as f:
            content = f.read()
        if not content:
            return [{}]
        return json.loads(content, object_pairs_hook=OrderedDict)

    def write(self, content):
        with open(self.config_file, 'w') as f:
            json.dump(content, f)

    def update(self, index, directives={}):
        content = self.read()
        count = len(content)
        if index < count:
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
