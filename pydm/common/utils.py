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
        path=os.path.realpath(path)
    try:
        out = execute('ls', '-l', path).split()
        disk = out[3]
        assert disk == 'disk', '%s is not a disk!' % path
        major = int(out[4][:-1])
        minor = int(out[5])
    except Exception, e:
        raise(e)
        return 0, 0
    else:
        return major, minor

def get_dev_sector_count(dev):
	if not os.path.exists(dev):
		raise Exception('Device %s does NOT exist...' % dev)
	devSector = execute('blockdev', '--getsz', dev)
	if type(devSector) != int:
		try:
			devSector = int(devSector)
		except:
			return 0
	if devSector <= 0:
		raise Exception('Device %s is EMPTY...' % dev)
	return devSector

def get_devname_from_major_minor(major_minor):
    return os.path.realpath('/dev/block/%s' % major_minor)

def write2tempfile(content):
	temp = tempfile.NamedTemporaryFile(delete=False)
	temp.write(content)
	temp.close()
	return temp.name


def bytes2sectors(bytes):
	bytes = bytes_str2bytes_count(bytes)
	sectors = bytes/512
	return sectors

def sector_offset2block_offset(startSector, offset, blkSize):
	blkSize = bytes_str2bytes_count(blkSize)
	startBlk = startSector * 512 / blkSize
	offsetBlk = offset * 512 / blkSize
	return startBlk, offsetBlk

def sectors2MB(sectors):
	return str(sectors*512/1024/1024) + 'M'
