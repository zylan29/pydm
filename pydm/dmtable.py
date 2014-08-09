from pydm.dmsetup import Dmsetup
from pydm.blockdev import Blockdev


class Table(object):
    def __init__(self, name, method, root_helper=''):
        self.root_helper = root_helper
        self.name = name
        self.method = method
        self.path = ''
        self.dm = Dmsetup(root_helper=root_helper)
        self.block = Blockdev(root_helper=root_helper)
        if self.dm.is_exist(self.name):
            self.existed = True
        else:
            self.existed = False

    def __str__(self):
        return NotImplementedError()

    def _parse_table(self):
        return NotImplementedError()

    def create_table(self):
        if self.existed:
            raise Exception("%s has been existed!" % self.name)
        else:
            self.path = self.dm.create_table(self.name, str(self))
            self.existed = True

    def remove_table(self):
        if not self.existed:
            raise Exception("%s does NOT exist!" % self.name)
        else:
            self.dm.remove_table(self.name)

    def reload_table(self):
        self.dm.reload_table(self.name, str(self))