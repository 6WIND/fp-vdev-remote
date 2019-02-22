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

from fp_vdev_remote import constants


FP_VDEV_CMD = None
FP_VDEV_CMD_CHECK = False


def command_exists(cmd):
    p = subprocess.Popen(['which', cmd], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if stderr:
        return None
    return stdout.strip()


def get_vdev_cmd():
    global FP_VDEV_CMD
    global FP_VDEV_CMD_CHECK
    if FP_VDEV_CMD_CHECK is False:
        FP_VDEV_CMD = command_exists(constants.FP_VDEV)
        if FP_VDEV_CMD is None:
            FP_VDEV_CMD = command_exists(constants.FP_VDEV_RMT)
        FP_VDEV_CMD_CHECK = True
    return FP_VDEV_CMD

