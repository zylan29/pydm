from pydm.dmtable import Table


class DmMultipath(Table):

    def __init__(self, name, root_helper=''):
        super(DmMultipath, self).__init__(name, 'multipath', root_helper=root_helper)
        if self.existed:
            self._parse_table()
        else:
            self.size = 0
            self.disks = []

    def __str__(self):
        count = len(self.disks)
        multipath_table = '0 %d multipath 0 0 1 1 queue-length 0 %d 1 ' % (self.size, count)
        for disk in self.disks:
            multipath_table += disk + ' 128 '
        return multipath_table

    def _parse_table(self):
        #TODO: to be continued...
        return NotImplementedError()