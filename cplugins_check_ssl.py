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

# import mandatory modules
# import cplugins
import argparse

from cplugins import cp_ssl, cp_output, cp_perfdata, cp_options

# define specific command line arguments
options = argparse.ArgumentParser(parents=[cp_options.CpOptions().parser])
local_group = options.add_argument_group('Specific options')
local_group.add_argument('--issuer', help='Check for SSL certificate issuer')
local_group.add_argument(
    '-p', '--port', help='Port to connect.', default='443'
)
local_group.add_argument('--subject', help='Check for SSL certificate subject')
local_group.add_argument(
    '--no-validity',
    help='Do not check SSL certificate duration',
    action='store_true'
)
args = options.parse_args()

# initiate output and perfdata
out = cp_output.CpOutput()
perf = cp_perfdata.CpPerfdata()
ssl = cp_ssl.CpSSL(args.host, args.port)

# build output
if not args.no_validity:
    out.add_short(
        'Certificate expires for \'{}\' in days: {} - Validity Date: {}'.
        format(
            ssl.get_subject(), ssl.get_expiration_from_now(),
            ssl.get_expiration_date()
        )
    )

if args.subject is not None:
    if args.subject == ssl.get_subject():
        out.add_short('Certificate subject is valid')
    else:
        out.add_short('Invalid subject', status='critical')

if args.issuer is not None:
    if args.issuer == ssl.get_issuer():
        out.add_short('Certificate issuer is valid')
    else:
        out.add_short('Invalid issuer', status='critical')

out.render()
