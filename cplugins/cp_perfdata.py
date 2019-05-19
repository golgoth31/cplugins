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

from .cp_common import CpCommon
from .cp_output import CpOutput


class CpPerfdata():
    def __init__(self):
        self.commons = CpCommon()
        self.out = CpOutput()
        self.args = self.out.args
        self._start = None
        self._end = None
        self._inside = 0
        self._error = 0
        self.data = []
        self._perf_status = []
        self._value = None
        self._precision = 2

    def _compute(self, threshold, status):
        self._parse_threshold(threshold)
        if not self._inside:
            if (self._end is not None and self._value > self._end) or \
                    (self._start is not None and self._value < self._start):
                self._perf_status.append(status)
                self._error = 1
        else:
            if self._value >= self._start and self._value <= self._end:
                self._perf_status.append(status)
                self._error = 1

    def _parse_threshold(self, threshold):
        try:
            try:
                self._end = self.commons.conv2number(threshold)
                self._start = 0
                return
            except ValueError:
                self._start, self._end = threshold.split(':')
                if self._start.startswith('@'):
                    self._inside = 1
                    self._start = self._start.strip('@')
                    self._start = self.commons.conv2number(self._start)
                    self._end = self.commons.conv2number(self._end)
                    if self._start > self._end:
                        raise ValueError("start can't be superior to end")
                else:
                    try:
                        self._start = self.commons.conv2number(self._start)
                    except ValueError:
                        self._start = None
                    try:
                        self._end = self.commons.conv2number(self._end)
                    except ValueError:
                        self._end = None
        except ValueError as error:
            print('bad threshold: ' + str(error))
            exit(3)

    def add(
        self,
        value,
        critical='',
        warning='',
        unit='',
        lmin='',
        lmax='',
        output=None,
        perfname='Value',
        info=None
    ):
        # if info given will overwrite warning, critical, min or max individual value
        self._error = 0
        data = {
            'perfname': '',
            'value': '',
            'unit': '',
            'warning': '',
            'critical': '',
            'min': '',
            'max': ''
        }
        try:
            self._value = self.commons.conv2number(value)
            data['perfname'] = perfname
            data['value'] = self.commons.conv2str(value)
            data['unit'] = unit
            data['warning'] = warning
            data['critical'] = critical
            data['min'] = str(lmin)
            data['max'] = str(lmax)
            if info is not None:
                temp_data = info.split(',')
                data['unit'] = temp_data[0]
                data['warning'] = temp_data[1]
                data['critical'] = temp_data[2]
                data['min'] = temp_data[3]
                data['max'] = temp_data[4]
            if data['warning'] is not '':
                warning = self.commons.conv2number(data['warning'])
                self._compute(warning, 'warning')
            if data['critical'] is not '':
                critical = self.commons.conv2number(data['critical'])
                self._compute(critical, 'critical')
            self.data.append(data)

            if self._error:
                if output is None:
                    output = perfname
                self.out.add_short(
                    output, status=self.out.worststatus(self._perf_status)[1]
                )
        except ValueError as e:
            print(e)
            exit(3)

    def human(self, value, unit=None, factor=1000):
        """Convert value to be human readable"""
        val = self.commons.conv2number(value)
        factor = self.commons.conv2number(factor)
        units = ['k', 'M', 'G', 'T', 'P', 'E']
        index = -1
        while val >= factor:
            val = val / factor
            index += 1
        if int(val) == float(val):
            text = str(int(val))
        else:
            text = format(val, '.' + str(self._precision) + 'f').strip('0')
        if index > -1:
            text += units[index]
        if unit is not None:
            text += unit
        return text
