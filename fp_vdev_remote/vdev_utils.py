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
import fnmatch
import os
import subprocess
import configparser

from distutils.spawn import find_executable

_REL_CFG_PATH = '../../etc'
_FPDEVRMT_INI = 'fp-vdev-remote.ini'
FP_RPCD_SOCK = '/var/run/fp_rpcd/fp-rpcd.sock'
FP_VDEV = 'fp-vdev'
FP_VDEV_RMT = 'fp-vdev-remote'

#-------------------------------------------------------------------------------
def get_config_path():
    fpvdevrmt_exec = find_executable('fp-vdev-remote')
    fpvdevrmt_path = os.path.join(os.path.dirname(fpvdevrmt_exec),
                                  _REL_CFG_PATH)
    fpvdevrmt_opts = os.path.join(fpvdevrmt_path, _FPDEVRMT_INI)
    return fpvdevrmt_opts

#-------------------------------------------------------------------------------
def get_conf():
    Config = configparser.ConfigParser()
    cfg_path = get_config_path()
    Config.read(cfg_path)
    cfg = {'FP_RPCD_SOCK': FP_RPCD_SOCK}
    try:
        fp_rpcd_dir = Config.get('rpcd', 'fp_rpcd_dir')
        if fp_rpcd_dir:
            cfg['FP_RPCD_SOCK'] = os.path.join(fp_rpcd_dir,
                                               os.path.basename(FP_RPCD_SOCK))
    except:
        # silently return default FP_RPCD_SOCK if fp_rpcd_dir or
        # fp-vdev-remote.ini were not found
        pass

    return cfg

# ------------------------------------------------------------------------------
def command_exists(cmd):
    p = subprocess.Popen(['which', cmd], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    _, stderr = p.communicate()
    if stderr:
        return False
    return True

# ------------------------------------------------------------------------------
def get_vdev_cmd():
    if command_exists(FP_VDEV):
        return FP_VDEV
    elif command_exists(FP_VDEV_RMT):
        return FP_VDEV_RMT
    else:
        return None

#-------------------------------------------------------------------------------
def get_rpcd_sock():
    # check if default/updated path exists
    if os.path.exists(FP_RPCD_SOCK):
        return FP_RPCD_SOCK
    # try to update path from conf
    cfg = get_conf()
    sockpath = cfg.get('FP_RPCD_SOCK')
    if os.path.exists(sockpath):
        return sockpath
    else:
        # perform lookup to '/run',
        # if you change FP_RPCD_SOCK default, please, take attention to the
        # obtained dirs value, just not to preform lookup to '/'
        dirs, sockname = os.path.split(FP_RPCD_SOCK)
        for dir, subdir, filelist in os.walk(os.path.dirname(dirs)):
            if [file for file in filelist if fnmatch.fnmatch(file, sockname)]:
                return os.path.join(dir, sockname)

    return FP_RPCD_SOCK
