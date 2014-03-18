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
        disk, major_minor = execute('ls', '-l', path, '|awk \'{print $4 "\t"  $5$6}\'').split('\t')
        assert disk == 'disk', '%s is not a disk!' % path
    except Exception, e:
        print e
        return 0, 0
    else:
        major, minor = map(int, major_minor.split(','))
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
	#return '/dev/' + os.readlink('/dev/block/%s' % major_minor)[3:]
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
