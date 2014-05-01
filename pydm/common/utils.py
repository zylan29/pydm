#!/usr/bin/env python

import os
import tempfile

from pydm.common import processutils as putils


def execute(cmd, *args, **kwargs):
    (out, ret) = putils.execute(cmd, *args, **kwargs)
    out = out.strip()
    return out


def get_major_minor(path):
    if os.path.islink(path):
        path = os.path.realpath(path)
    try:
        out = execute('ls', '-l', path).split()
        disk = out[3]
        assert disk == 'disk', '%s is not a disk!' % path
        major = int(out[4][:-1])
        minor = int(out[5])
    except Exception, e:
        raise e
        return 0, 0
    else:
        return major, minor


def get_devname_from_major_minor(major_minor):
    return os.path.realpath('/dev/block/%s' % major_minor)


def write2tempfile(content):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(content)
    temp.close()
    return temp.name


def sectors2MB(sectors):
    return str(sectors * 512 / 1024 / 1024) + 'M'
