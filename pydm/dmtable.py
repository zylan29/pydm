from pydm.disk import Disk
from pydm.dmsetup import Dmsetup


class LinearTable:
    def __init__(self, name, root_helper=''):
        self.root_helper = root_helper
        self.name = name
        self.disks = []
        self.path = ''
        self.dm = Dmsetup(root_helper=root_helper)
        self.existed = False

        if self.dm.is_exist(self.name):
            self.existed = True
            self.path = '/dev/mapper/%s' % self.name
            table = self.dm.get_table(self.name)
            self.disks = self._parse_table(table)

    def __str__(self):
        self._compute_starts()
        return '\n'.join(map(str, self.disks))

    def _parse_table(self, table):
        disks = []
        lines = table.split('\n')
        for line in lines:
            disk = Disk.from_line(line, root_helper=self.root_helper)
            if disk:
                disks.append(disk)
        return disks

    def _compute_starts(self):
        start = 0
        for disk in self.disks:
            disk.start = start
            start += disk.size

    def reload_table(self):
        self.dm.reload_table(self.name, str(self))

    def create_table(self):
        if self.existed:
            raise Exception("%s has been existed! \n Try reload_table" % self.name)
        else:
            self.path = self.dm.create_table(self.name, str(self))
            self.existed = True

    def insert_disk(self, newdisk):
        for i in range(len(self.disks)):
            disk = self.disks[i]
            # find the first free space (mapper=='error') that is big enough
            if disk.mapper != 'error' or disk.size < newdisk.size:
                continue
            newdisk.start = disk.start
            if disk.size > newdisk.size:
                disk.size -= newdisk.size
                disk.start += newdisk.size
                self.disks.insert(i, newdisk)
            elif disk.size == newdisk.size:
                self.disks[i] = newdisk
            self.reload_table()
            return True
        return False

    def remove_disk(self, thedisk):
        length = len(self.disks)
        for i in range(length):
            disk = self.disks[i]
            if disk.major_minor == thedisk.major_minor:
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

    def find_disk(self, thedisk):
        if not isinstance(thedisk, Disk):
            thedisk = Disk.from_path(thedisk, root_helper=self.root_helper)
        for disk in self.disks:
            if disk.major_minor == thedisk.major_minor:
                return disk
        return None

    @staticmethod
    def from_disks(name, disks, root_helper=''):
        linear_table = LinearTable(name, root_helper=root_helper)
        for disk in disks:
            if type(disk) == str:
                linear_table.disks.append(Disk.from_path(disk, root_helper=root_helper))
            elif isinstance(disk, Disk):
                linear_table.disks.append(disk)
            else:
                raise Exception("Unknown type of %s" % disk)
        linear_table.create_table()
        return linear_table
