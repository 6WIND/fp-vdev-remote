#    Copyright 2019 6WIND S.A.
#    All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import subprocess


FP_RPCD_SOCKET_PATH = '/run/openvswitch/fp-rpcd.sock'
FP_VDEV = 'fp-vdev'
FP_VDEV_RMT = 'fp-vdev-remote'


def command_exists(cmd):
    p = subprocess.Popen(['which', cmd], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    _, stderr = p.communicate()
    if stderr:
        return False
    return True


def get_vdev_cmd():
    if command_exists(FP_VDEV):
        return FP_VDEV
    elif command_exists(FP_VDEV_RMT):
        return FP_VDEV_RMT
    else:
        return None
