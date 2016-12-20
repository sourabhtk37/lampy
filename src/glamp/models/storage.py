import json
import os
from collections import OrderedDict


class Sites(object):
    def __init__(self):
        self.file = self.file("sites.json")
        if not os.path.isfile(self.file):
            if not os.path.exists(os.path.dirname(self.file)):
                os.makedirs(os.path.dirname(self.file))
            open(self.file, 'a').close()

    def file(self, filename):
        return os.path.join(os.path.expanduser("~/.glamp"), filename)

    def read(self):
        with open(self.file, 'r') as f:
            content = f.read()
        if not content:
            return []
        return json.loads(content, object_pairs_hook=OrderedDict)

    def write(self, content):
        with open(self.file, 'w') as f:
            json.dump(content, f)

    def update(self, index, properties={}):
        content = self.read()
        count = len(content)
        if index < count:
            content[index].update(properties)
        self.write(content)

    def remove(self, index=[]):
        if index:
            content = self.read()
            for i in sorted(index, reverse=True):
                if i < len(content):
                    del content[i]
            self.write(content)
