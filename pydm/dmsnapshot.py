from blockdev import Blockdev
from dmtable import Table


class DmOrigin(Table):

    def __init__(self, name, root_helper=''):
        super(DmOrigin, self).__init__(name, 'snapshot-origin', root_helper=root_helper)
        if self.existed:
            self._parse_table()
        else:
            self.origin_dev = ''
            self.origin_size = 0

    def __str__(self):
        if self.origin_size == 0:
            raise ValueError('%s is EMPTY!' % self.origin_dev)
        return '0 %d snapshot-origin %s' % (self.origin_size, self.origin_dev)

    def _parse_table(self):
        table = self.dm.get_table(self.name)
        [_, size, _, major_minor] = table.split()
        self.origin_dev = self.block.get_path_from_major_minor(major_minor)
        self.origin_size = int(size)

    def _set_origin_dev(self, origin_dev=''):
        if origin_dev and origin_dev != self.origin_dev:
            self.origin_dev = origin_dev
            block = Blockdev(root_helper=self.root_helper)
            self.origin_size = block.get_sector_count(self.origin_dev)

    def create_origin(self, origin_dev=''):
        self._set_origin_dev(origin_dev)
        self.create_table()

    def remove_origin(self):
        self.remove_table()


class DmSnapshot(Table):
    """
    Snapshot based on device mapper.
    """
    def __init__(self, name, root_helper=''):
        super(DmSnapshot, self).__init__(name, 'snapshot', root_helper=root_helper)
        if self.existed:
            self._parse_table()
        else:
            self.origin_dev = ''
            self.origin_size = 0
            self.snapshot_dev = ''

    def __str__(self):
        if self.origin_size == 0:
            raise ValueError('%s is EMPTY!' % self.origin_dev)
        return '0 %d snapshot %s %s N 128' % (self.origin_size, self.origin_path, self.snapshot_dev)

    def _parse_table(self):
        table = self.dm.get_table(self.name)
        [_, origin_size, _, origin_major_minor, snapshot_major_minor, _, _] = table.split()
        self.origin_dev = self.block.get_major_minor(origin_major_minor)
        self.origin_size = int(origin_size)
        self.snapshot_dev = self.block.get_path_from_major_minor(snapshot_major_minor)

    def create_snapshot(self, origin_dev, snapshot_dev):
        self.origin_dev = origin_dev
        self.origin_size = self.block.get_sector_count(origin_dev)
        self.snapshot_dev = snapshot_dev
        self.create_table()

    def remove_snapshot(self):
        self.remove_table()