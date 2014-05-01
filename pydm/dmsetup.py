#!/usr/bin/env python

from pydm.common import executor
from pydm.common import processutils as putils
from pydm.common import utils
from pydm.blockdev import Blockdev


class Dmsetup(executor.Executor):
    def __init__(self, mapdev_prefix='/dev/mapper/', root_helper='', execute=putils.execute):
        super(Dmsetup, self).__init__(root_helper, execute=execute)
        self.mapdev_prefix = mapdev_prefix

    def _run_dmsetup(self, dmsetup_command, *args):
        (out, err) = self._execute('dmsetup', dmsetup_command, *args, run_as_root=True, root_helper=self._root_helper)
        out = out.strip()
        return out, err

    def is_exist(self, name):
        try:
            self.get_table(name)
        except Exception, e:
            return False
        else:
            return True

    def create_table(self, name, table):
        table_file = utils.write2tempfile(table)
        self._run_dmsetup('create', name, table_file)
        return self.mapdev_prefix + name

    def remove_table(self, name):
        self._run_dmsetup('remove', name)

    def reload_table(self, name, table):
        table_file = utils.write2tempfile(table)
        self._run_dmsetup('suspend', name)
        self._run_dmsetup('reload', name, table_file)
        self._run_dmsetup('resume', name)

    def show_table(self):
        (out, ret) = self._run_dmsetup('table')
        return out

    def get_table(self, name):
        (out, ret) = self._run_dmsetup('table', name)
        return out

    def origin(self, origin_name, origin_dev):
        block = Blockdev(root_helper=self._root_helper)
        origin_size = block.get_sector_count(origin_dev)
        origin_table = '0 %d snapshot-origin %s' % (origin_size, origin_dev)
        self.create_table(origin_name, origin_table)
        origin_path = self.mapdev_prefix + origin_name
        return origin_path

    def snapshot(self, origin_path, snapshot_name, snapshot_dev):
        block = Blockdev(root_helper=self._root_helper)
        origin_size = block.get_sector_count(origin_path)
        snapshot_size = block.get_sector_count(snapshot_dev)
        snapshot_table = '0 %d snapshot %s %s N 128' % (origin_size, origin_path, snapshot_dev)
        self.create_table(snapshot_name, snapshot_table)
        snapshot_path = self.mapdev_prefix + snapshot_name
        return snapshot_path

    def multipath(self, name, disks):
        multipath_table = ''
        block = Blockdev(root_helper=self._root_helper)
        size = block.get_sector_count(disks[0])
        count = len(disks)
        multipath_table += '0 %d multipath 0 0 1 1 queue-length 0 %d 1 ' % (size, count)
        for disk in disks:
            multipath_table += disk + ' 128 '
        multipath_table += '\n'
        self.create_table(name, multipath_table)
        return self.mapdev_prefix + name