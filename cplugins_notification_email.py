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

import argparse
from cplugins import cp_options, cp_notification

# define specific command line arguments
OPTIONS = argparse.ArgumentParser(parents=[cp_options.CpOptions().parser])
LOCAL_GROUP = OPTIONS.add_argument_group('Specific options')
LOCAL_GROUP.add_argument(
    '-t', '--template', help='template to be used', default='default'
)
LOCAL_GROUP.add_argument('--to', help='send email to', required=True)
LOCAL_GROUP.add_argument(
    '--list-templates', help='template to be used', action='store_true'
)

ARGS = OPTIONS.parse_args()

NOTIF = cp_notification.CpNotification('CpEmail', args=ARGS)
NOTIF.sendEmail()
