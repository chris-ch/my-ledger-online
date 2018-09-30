"""
Test cases for the oasclient package.

@author: Christophe Alexandre <optimacom.sarl at gmail dot com>

@license:
Copyright(C) 2010 Optimacom sarl

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.    If not, see <http://www.gnu.org/licenses/lgpl.txt>.
"""

import unittest
import logging
from pprint import pprint
from datetime import datetime


class OASClientTest(unittest.TestCase):
    def test_positional(self):
        from oasclient.jsonext import ServiceProxy
        rpc_srv = ServiceProxy('localhost', 'jsonrpc', port=8080, version='2.0')
        result = rpc_srv.subtract(42, 23)
        self.assertEquals(result, 19)

    def test_named_1(self):
        from oasclient.jsonext import ServiceProxy
        rpc_srv = ServiceProxy('localhost', 'jsonrpc', port=8080, version='2.0')
        result = rpc_srv.subtract(subtrahend=23, minuend=42)
        self.assertEquals(result, 19)

    def test_named_2(self):
        from oasclient.jsonext import ServiceProxy
        rpc_srv = ServiceProxy('localhost', 'jsonrpc', port=8080, version='2.0')
        result = rpc_srv.subtract(minuend=42, subtrahend=23)
        self.assertEquals(result, 19)


if __name__ == '__main__':
    unittest.main()
