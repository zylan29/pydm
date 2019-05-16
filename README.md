What's pydm
======

A python wrapper for linux device mapper command(dmsetup).


Features of pydm
------

* Execute dmsetup in your python script.
* Easy to use, avoid fussy arguments of the command.
* Supported multiple mapping methods.
  1. Linear
  * Snapshot
  * Multipath

How to get pydm
------

  > git clone https://github.com/zylan29/pydm.git

Installation
------
```
python setup.py install
```

Sample usage
======
Linear
------
Build linear map from two hard disks:
```python
from pydm.dmlinear import DmLinearTable
hdd_group = DmLinearTable.from_disks(group_name, [hdd_1, hdd_2], root_helper='sudo')
```
Snapshot
------

Multipath
------
Related Projects
======
flashcachegroup: Making FB's flashcache to cache a group of disks with a single SSD

  > https://github.com/lihuiba/flashcachegroup

vritman: Booting 1000 VMs in a minute!
  > http://www.vmthunder.org

  > https://github.com/vmthunder/virtman
