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
import http.client as http_cli
import os
import socket
import sys
import xmlrpc.client as xrpc_cli

from fp_vdev_remote import vdev_utils


class UnixStreamHTTPConnection(http_cli.HTTPConnection):
    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.host)


class UnixStreamTransport(xrpc_cli.Transport, object):
    def __init__(self, sockfile):
        self.socket_path = sockfile
        super(UnixStreamTransport, self).__init__()

    def make_connection(self, host):
        return UnixStreamHTTPConnection(self.socket_path)


def main():
    parser = argparse.ArgumentParser(prog=vdev_utils.FP_VDEV_RMT,
                                     description='Run fp-vdev utilities on '
                                     'remote through XMLRPC')
    _, unknown_args = parser.parse_known_args()

    args = ' '.join(unknown_args)

    # Set the first argument to 'http://' to let xmlrpc.client.Server happy.
    # Not needed in our case as we use a UNIX socket as transport
    s = xrpc_cli.Server('http://',
                         transport=UnixStreamTransport(vdev_utils.get_rpcd_sock()))
    ret, out, err = s.fp_vdev_cmd(args)
    sys.stderr.write(err)
    sys.stdout.write(out)
    return ret
