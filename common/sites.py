import os
import json
from collections import OrderedDict


class Sites(object):
    def __init__(self):
        self.file = self.file()
        if not os.path.exists(os.path.dirname(self.file)):
            os.makedirs(os.path.dirname(self.file))

    @staticmethod
    def file():
        return os.path.expanduser('~') + '/.glampy/sites.json'

    def read(self):
        with open(self.file, 'r') as f:
            content = f.read()
        if not content:
            return [{}]
        return json.loads(content, object_pairs_hook=OrderedDict)

    def write(self, content):
        with open(self.file, 'w') as f:
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
