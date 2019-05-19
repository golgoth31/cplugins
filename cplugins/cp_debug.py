# -*- coding: utf-8 -*-

# Cplugins
# Copyright (c) 2016 David Sabatie <github@notrenet.com>
#
# This file is part of Cplugins.
#
# Cplugins is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cplugins is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import logging
from .cp_options import CpOptions


class CpDebug():
    def __init__(self):
        self.args = CpOptions().parser.parse_args()
        self.debug = logging.getLogger('debug')
        debug = logging.StreamHandler()
        debug.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        debug.setFormatter(formatter)
        self.debug.addHandler(debug)
        if self.args.log:
            self.debug.addHandler(self.log())

    def log(self):
        log = logging.FileHandler(self.args.log)
        log.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        log.setFormatter(formatter)
        return log
