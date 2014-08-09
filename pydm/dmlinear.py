from pydm.lineardisk import LinearDisk
from dmtable import Table


class DmLinearTable(Table):
    """
    An abstract for linear map table.
    """
    def __init__(self, name, root_helper=''):
        super(DmLinearTable, self).__init__(name, 'linear', root_helper=root_helper)
        if self.existed:
            self.path = '/dev/mapper/%s' % self.name
            self.disks = self._parse_table()
        else:
            self.disks = []

    def __str__(self):
        return '\n'.join(map(str, self.disks))

    def _parse_table(self):
        table = self.dm.get_table(self.name)
        disks = []
        lines = table.split('\n')
        for line in lines:
            disk = LinearDisk.from_line(line, root_helper=self.root_helper)
            if disk:
                disks.append(disk)
        return disks

    def find_disk(self, the_disk):
        if not isinstance(the_disk, LinearDisk):
            the_disk = LinearDisk.from_path(the_disk, root_helper=self.root_helper)
        for disk in self.disks:
            if disk.major_minor == the_disk.major_minor:
                return disk
        return None

    def insert_disk(self, new_disk):
        return NotImplementedError()

    def remove_disk(self, the_disk):
        return NotImplementedError()

    @staticmethod
    def from_disks(name, disks, root_helper='', cls=None):
        if not cls:
            cls = DmLinearTable
        linear_table = cls(name, root_helper=root_helper)
        for disk in disks:
            if type(disk) == str:
                linear_table.disks.append(LinearDisk.from_path(disk, root_helper=root_helper))
            elif isinstance(disk, LinearDisk):
                linear_table.disks.append(disk)
            else:
                raise Exception("Unknown type of %s" % disk)
        linear_table.create_table()
        return linear_table


class CommonDmLinearTable(DmLinearTable):
    """
    A common realization for linear table.
    """
    def __init__(self, name, root_helper=''):
        super(CommonDmLinearTable, self).__init__(name, root_helper=root_helper)

    def __str__(self):
        self._compute_starts()
        return '\n'.join(map(str, self.disks))

    def _compute_starts(self):
        start = 0
        for disk in self.disks:
            disk.start = start
            start += disk.size

    def insert_disk(self, new_disk):
        """
        Insert new disk to the first big enough space.
        :param new_disk:
        :return: True if insert successful, otherwise false.
        """
        for i in range(len(self.disks)):
            disk = self.disks[i]
            # find the first free space (mapper=='error') that is big enough
            if disk.mapper != 'error' or disk.size < new_disk.size:
                continue
            new_disk.start = disk.start
            if disk.size > new_disk.size:
                disk.size -= new_disk.size
                disk.start += new_disk.size
                self.disks.insert(i, new_disk)
            elif disk.size == new_disk.size:
                self.disks[i] = new_disk
            self.reload_table()
            return True
        return False

    def remove_disk(self, the_disk):
        length = len(self.disks)
        for i in range(length):
            disk = self.disks[i]
            if disk.major_minor == the_disk.major_minor:
                disk.set_error()
                pre_disk = None
                post_disk = None
                if i >= 1:
                    pre_disk = self.disks[i - 1]
                if i < length - 1:
                    post_disk = self.disks[i + 1]
                for adisk in [pre_disk, post_disk]:
                    if adisk:
                        if adisk.mapper == 'error':
                            disk.size += adisk.size
                            self.disks.remove(adisk)
                self.reload_table()
                return True
        return False

    @staticmethod
    def from_disks(name, disks, root_helper=''):
        linear_table = DmLinearTable.from_disks(name, disks, root_helper=root_helper, cls=CommonDmLinearTable)
        return linear_table
