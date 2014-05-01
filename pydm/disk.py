
import os

from pydm.common import utils


class Disk: 
    def __init__(self):
        self.start = 0
        self.size = 0
        self.mapper = ''
        self.dev = ''
        self.offset = 0
        self.major_minor = ''
        self.major = 0
        self.minor = 0

    def __str__(self):
        return '%d %d %s %s %d' % (self.start, self.size, self.mapper, self.dev, self.offset)

    def set_error(self):
        self.mapper = 'error'
        self.dev = ''
        self.major_minor = ''
        self.major = 0
        self.minor = 0


    @staticmethod
    def from_error(size):
        disk = Disk()
        disk.size = size
        disk.set_error()
        return disk

    @staticmethod
    def from_path(path):
        if os.path.exists(path):
            disk = Disk()
            disk.dev = os.path.realpath(path)
            disk.size = utils.get_dev_sector_count(disk.dev)
            disk.major, disk.minor = utils.get_major_minor(disk.dev)
            disk.major_minor = ':'.join(map(str, [disk.major, disk.minor]))
            disk.mapper = 'linear'
            
            return disk
        else:
            raise Exception('disk %s does NOT exist!'%path)

    @staticmethod
    def from_line(line):
        disk = Disk()
        line_list = line.split()
        length = len(line_list)
        disk.size = int(line_list[1])
        disk.mapper = line_list[2]

        if length == 5:
            disk.major_minor = line_list[3]
            disk.dev = utils.get_devname_from_major_minor(disk.major_minor)
            disk.offset = int(line_list[4])
        return disk
