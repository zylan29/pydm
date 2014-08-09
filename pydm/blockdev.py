#!/usr/bin/env python
import os

from pydm.common import executor
from pydm.common import processutils as putils


class Blockdev(executor.Executor):

    def __init__(self, root_helper='', execute=putils.execute):
        super(Blockdev, self).__init__(root_helper, execute=execute)

    def _run_blockdev(self, *args):
        (out, err) = self._execute('blockdev', *args, run_as_root=True, root_helper=self._root_helper)
        out = out.strip()
        return out

    def get_sector_count(self, dev):
        if not os.path.exists(dev):
            raise Exception('Device %s does NOT exist...' % dev)
        dev_sector = self._run_blockdev('--getsz', dev)
        if not isinstance(dev_sector, int):
            try:
                dev_sector = int(dev_sector)
            except ValueError:
                return 0
        if dev_sector <= 0:
            raise Exception('Device %s is EMPTY...' % dev)
        return dev_sector

    def get_major_minor(self, dev):
        if os.path.islink(dev):
            dev = os.path.realpath(dev)
        try:
            (out, ret) = self._execute('ls', '-l', dev)
            out = out.strip().split()
            disk = out[3]
            assert disk == 'disk', '%s is not a disk!' % dev
            major = int(out[4][:-1])
            minor = int(out[5])
        except Exception, e:
            raise e
        else:
            return major, minor

    def get_path_from_major_minor(self, major, minor=''):
        disk_prefix = '/dev/block/'
        if minor:
            if major.find(':') == -1:
                major_minor = str(major) + ':' + str(minor)
            else:
                raise ValueError()
        else:
            if major.find(':') == -1:
                raise ValueError()
            else:
                major_minor = major
        path = os.readlink(disk_prefix + major_minor)
        path = os.path.realpath(disk_prefix + path)
        return path