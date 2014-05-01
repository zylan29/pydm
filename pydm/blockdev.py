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
        return out, err

    def get_sector_count(self, dev):
        if not os.path.exists(dev):
            raise Exception('Device %s does NOT exist...' % dev)
        dev_sector = self._run_blockdev('--getsz', dev)
        if not isinstance(dev_sector, int):
            try:
                dev_sector = int(dev_sector)
            except Exception, e:
                return 0
        if dev_sector <= 0:
            raise Exception('Device %s is EMPTY...' % dev)
        return dev_sector

    def get_major_minor(self, dev):
        if os.path.islink(dev):
            path = os.path.realpath(dev)
        try:
            out = self._execute('ls', '-l', path).split()
            disk = out[3]
            assert disk == 'disk', '%s is not a disk!' % path
            major = int(out[4][:-1])
            minor = int(out[5])
        except Exception, e:
            raise e
        else:
            return major, minor