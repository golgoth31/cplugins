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
# import sys


class CpCommon():
    """ Common functions for cplugins sdk """

    def __init__(self):
        pass

    def is_number(self, s):
        """ Check if a value is numeric or not """
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def conv2number(self, s):
        """ Convert a value to float if possible """
        try:
            return float(s)
        except ValueError as e:
            print(e)
            pass

        try:
            import unicodedata
            return unicodedata.numeric(s)
        except (TypeError, ValueError):
            pass

        raise ValueError("Can't convert value to numeric")

    def conv2str(self, s):
        """ Convert a value to string """
        try:
            return str(s)
        except ValueError:
            pass

        try:
            import unicodedata
            return unicodedata.string(s)
        except (TypeError, ValueError):
            pass

        raise ValueError("Can't convert value to string")
