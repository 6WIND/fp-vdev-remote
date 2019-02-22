# Copyright 2019 6WIND S.A.
# All Rights Reserved.
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

import argparse
import httplib
import os
import socket
import sys
import xmlrpclib

from vdev_utils import FP_RPCD_SOCKET_PATH
from vdev_utils import FP_VDEV_RMT


class UnixStreamHTTPConnection(httplib.HTTPConnection):
    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.host)


class UnixStreamTransport(xmlrpclib.Transport, object):
    def __init__(self, FP_RPCD_SOCKET_PATH):
        self.socket_path = FP_RPCD_SOCKET_PATH
        super(UnixStreamTransport, self).__init__()

    def make_connection(self, host):
        return UnixStreamHTTPConnection(self.socket_path)


def main():
    parser = argparse.ArgumentParser(prog=FP_VDEV_RMT,
                                     description='Run fp-vdev utilities on '
                                     'remote through XMLRPC')
    _, unknown_args = parser.parse_known_args()

    args = ' '.join(unknown_args)

    # Set the first argument to 'http://' to let xmlrpclib.Server happy.
    # Not needed in our case as we use a UNIX socket as transport
    s = xmlrpclib.Server('http://',
                         transport=UnixStreamTransport(FP_RPCD_SOCKET_PATH))

    ret, out, err = s.fp_vdev_cmd(args)
    sys.stderr.write(err)
    sys.stdout.write(out)
    return ret
