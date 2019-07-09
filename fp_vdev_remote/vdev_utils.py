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
import os
import subprocess
import ConfigParser

from distutils.spawn import find_executable

_REL_CFG_PATH = '../../etc'
_FPDEVRMT_INI = 'fp-vdev-remote.ini'
FP_RPCD_DIR = '/var/run/fp_rpcd'
FP_VDEV = 'fp-vdev'
FP_VDEV_RMT = 'fp-vdev-remote'
SOCKFILE = 'fp-rpcd.sock'


def get_config_path():
    fpvdevrmt_exec = find_executable('fp-vdev-remote')
    fpvdevrmt_path = os.path.join(os.path.dirname(fpvdevrmt_exec),
                                  _REL_CFG_PATH)
    fpvdevrmt_opts = os.path.join(fpvdevrmt_path, _FPDEVRMT_INI)
    return fpvdevrmt_opts

#------------------------------------------------------------------------------
def get_conf():
    Config = ConfigParser.ConfigParser()
    cfg_path = get_config_path()
    Config.read(cfg_path)
    cfg = {'FP_RPCD_DIR': FP_RPCD_DIR}
    try:
        cfg['FP_RPCD_DIR'] = Config.get('rpcd', 'fp_rpcd_dir')
    except:
        # silently return default value if fp_rpcd_dir or fp-vdev-remote.ini
        # were not found
        pass
    return cfg


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
