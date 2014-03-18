
from pydm.disk import Disk
from pydm.dmsetup import Dmsetup

class LinearTable():
    def __init__(self, name):
        self.name = name
        self.disks = []
        self.dm = Dmsetup()

        if self.dm.is_exist(self.name):
            table = self.dm.get_table(self.name)
            self.disks = self._parse_table(table)

    def __str__(self):
        _compute_starts(self);
        return '\n'.join(map(str, self.disks))

    def _parse_table(self, table):
        disks = []
        lines = table.split('\n')
        for line in lines:
            disk = Disk.from_line(line)
            if disk:
                disks.append(disk)
        return disks

    def _compute_starts():
        start=0;
        for disk in self.disks:
            disk.start = start
            start += disk.size

    def _reload_table(self):
        dm.reload_table(self.name, str(self))

    def insert_disk(self, newdisk):
        for i in range(len(self.disks)):
            disk = self.disks[i]
            # find the first free space (mapper=='error') that is big enough
            if disk.mapper != 'error' or disk.size < newdisk.size:
                continue
            newdisk.start = disk.start
            if disk.size>newdisk.size:
                disk.size -= newdisk.size
                disk.start += newdisk.size
                self.disks.insert(i, newdisk)
            elif disk.size == newdisk.size:
                self.disks[i]= newdisk
            self._reload()
            return True
        return False

    def remove_disk(self, thedisk):
        length = len(self.disks)
        for i in range(length):
            disk = self.disks[i]
            if disk.mapper =='linear' and disk.major_minor == thedisk.major_minor:
                disk.set_error()
                pre_disk = None
                post_disk = None
                if i >= 1:
                    pre_disk = self.disks[i-1]
                if i < length - 1:
                    post_disk = self.disks[i+1]
                for adisk in [pre_disk, post_disk]:
                    if adisk.mapper == 'error':
                        disk.size += adisk.size
                        self.disks.remove(adisk)
                self._reload()
                return True
        return False
