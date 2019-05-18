# -*- coding: utf-8 -*-

# pybroker
# Copyright (c) 2016 David Sabatie <pybroker@notrenet.com>
#
# This file is part of Pybroker.
#
# Foobar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import argparse


class CpOptions():
    def __init__(self):

        self.parser = argparse.ArgumentParser(
            description='Cplugins help text', add_help=False
        )

        default = self.parser.add_argument_group('default')
        default.add_argument(
            '-v', '--version', action='version', version='%(prog)s 1.0'
        )
        default.add_argument(
            '-d', '--debug', action='store_true', help='debug mode'
        )
        default.add_argument(
            '-H',
            '--host',
            help=
            'give the hostname to query. For email notification, this is the smtp relay',
            required=True
        )
        default.add_argument(
            '-l', '--long', help='generate long output', action='store_true'
        )
        default.add_argument('-L', '--log', help='generate log file')
        default.add_argument('--statefile', help='generate state file')
        default.add_argument(
            '-F',
            '--format',
            help='choose output format',
            choices=['nagios', 'json'],
            default='nagios'
        )