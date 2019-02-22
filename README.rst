==============
fp-vdev-remote 
==============

fp-vdev-remote is a Python module, which implements a CLI to fp-rcpd daemon.
fp-rcpd daemon is a part of 6WIND virtual-accelerator product, it is installing
in host-hypervisor with fastpath binaries and launching by virtual-accelerator
start script. It serves as a proxy to bypass fp-vdev requests from 6WIND
OpenStack plugins installed in containers to host-hypervisor, where fp-vdev
utility resides. fp-rpcd.sock should be created in a folder shared between all
OpenStack containers, which are using 6WIND plugins.

fp-vdev-remote sends fp-vdev plugin requests to fp-rpcd.sock and provides a
method to determine, which binary: fp-vdev or fp-vdev-remote should be used by
plugin by checking the presence of the fp-rpcd.sock file.

* Source: https://github.com/6WIND/fp-vdev-remote
* Bugs: http://bugs.launchpad.net/fp-vdev-remote
