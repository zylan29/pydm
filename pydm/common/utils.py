#!/usr/bin/env python

import os
import tempfile


def get_devname_from_major_minor(major_minor):
    return os.path.realpath('/dev/block/%s' % major_minor)


def write2tempfile(content):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(content)
    temp.close()
    return temp.name


def sectors2MB(sectors):
    return str(sectors * 512 / 1024 / 1024) + 'M'
