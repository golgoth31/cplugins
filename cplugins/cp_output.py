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
from .cp_options import CpOptions
from .cp_debug import CpDebug


class CpOutput():
    def __init__(self):
        self.default_output = 'Everything is OK'
        self.forced_output = None
        self.out_tab = []
        self.out_long_tab = []
        self.out_status = []
        self.out_statuses = {
            'OK': 0,
            'WARNING': 1,
            'CRITICAL': 2,
            'UNKNOWN': 3
        }
        self.args = CpOptions().parser.parse_known_args()

    def add_short(self, output, status=None):
        """adds a short output"""
        self.out_tab.append(output)
        self.out_status.append(status)

    def add_long(self, output):
        """adds a long output"""
        self.out_long_tab.append(output)

    def _render_nagios(self):
        # generate output text
        if not len(self.out_tab):
            output = self.default_output
        else:
            if self.forced_output is not None:
                output_text = self.forced_output + ', '
            else:
                output_text = ""
            for i in range(0, len(self.out_tab)):
                # if the status is not OK, print it
                if self.out_status[i] is not None and self.out_status[
                    i] is not 'ok':
                    output_text += self.out_status[i].upper() + ': '
                # add each output to the final text
                output_text += self.out_tab[i] + ', '
            output = output_text.rstrip(', ')
        output += ' | '
        # add perfdata if needed
        for perf in self.perfdata:
            output += "'" + perf['perfname'] + "'=" + perf['value'] + perf[
                'unit'] + ";" + perf['warning'] + ";" + perf[
                    'critical'] + ";" + perf['min'] + ";" + perf['max'] + " "

        # add long output if needed
        if self.args[0].long:
            for i in range(0, len(self.out_long_tab)):
                output += '\n' + self.out_long_tab[i]
        return output

    def _render_json(self):
        output_header = '{"output": {"short": ["'
        if not len(self.out_tab):
            output = output_header + self.default_output
        else:
            output = output_header
            if self.forced_output is not None:
                output += self.forced_output + '","'
            for i in range(0, len(self.out_tab)):
                # if the status is not OK, print it
                if self.out_status[i] is not None and self.out_status[
                    i] is not 'ok':
                    output += self.out_status[i].upper + ': '
                # add each output to the final text
                output += self.out_tab[i] + '","'
            output = output.rstrip(',"')
        output += '"],"long": ['

        # add long output
        if len(self.out_long_tab) > 0:
            output += '"'
            for i in range(0, len(self.out_long_tab)):
                output += self.out_long_tab[i] + '","'
            output = output.rstrip(',"')
            output += '"'

        output += ']},"perfdata": ['

        # add perfdata if needed
        if len(self.perfdata):
            output += '{"'
            for perf in self.perfdata:
                output += perf['perfname'] + '": {'
                output += '"value": "' + perf['value'] + '",'
                output += '"unit": "' + perf['unit'] + '",'
                output += '"warning": "' + perf['warning'] + '",'
                output += '"critical": "' + perf['critical'] + '",'
                output += '"min": "' + perf['min'] + '",'
                output += '"max": "' + perf['max'] + '"},"'
            output = output.rstrip(',"')
            output += '}'
        output += ']}'
        return output

    def render(self, perfdata=None):
        """Render the output and exit with the good status"""
        # Render perfdata if given
        if perfdata is not None:
            self.perfdata = perfdata.data
            for i in range(0, len(perfdata.out.out_tab)):
                self.out_status.append(perfdata.out.out_status[i])
                self.out_tab.append(perfdata.out.out_tab[i])
        else:
            self.perfdata = []
        # check for worststatus
        self.exit_status, self.exit_literal_status = self._worststatus(
            self.out_status
        )

        # print and exit
        print(getattr(self, '_render_' + self.args[0].format)())
        exit(self.exit_status)

    def _worststatus(self, status):
        """Compute the worst status in the output array.
        status: list of status; ex. ['ok', 'WARNING']
        """
        current_status = 0
        literal_status = 'OK'
        for i in range(0, len(status)):
            if status[i] is not None:
                local_status = status[i].upper()
                if self.out_statuses[local_status] > current_status:
                    current_status = self.out_statuses[local_status]
                    literal_status = local_status

        return [current_status, literal_status]
