#!/usr/bin/env python3
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

# from cplugins import CpOutput, CpPerfdata, CpOptions
from cplugins import cp_options, cp_notification
import argparse

# define specific command line arguments
options = argparse.ArgumentParser(parents=[cp_options.CpOptions().parser])
local_group = options.add_argument_group('Specific options')
local_group.add_argument(
    '-t', '--template', help='template to be used', default='default'
)
local_group.add_argument('--to', help='send email to', required=True)
local_group.add_argument(
    '--list-templates', help='template to be used', action='store_true'
)
local_group.add_argument(
    '-p',
    '--parameters',
    help='a list of parameters',
    nargs='+',
    required=True
)
args = options.parse_args()

notif = cp_notification.CpNotification('CpEmail', args=args)
notif.sendEmail()
