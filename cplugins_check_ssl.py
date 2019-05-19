#!/usr/bin/env python3
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

# import mandatory modules
import argparse

from cplugins import cp_ssl, cp_output, cp_perfdata, cp_options

# define specific command line arguments
OPTIONS = argparse.ArgumentParser(parents=[cp_options.CpOptions().parser])
LOCAL_GROUP = OPTIONS.add_argument_group('Specific options')
LOCAL_GROUP.add_argument('--issuer', help='Check for SSL certificate issuer')
LOCAL_GROUP.add_argument(
    '-p', '--port', help='Port to connect.', default='443'
)
LOCAL_GROUP.add_argument('--subject', help='Check for SSL certificate subject')
LOCAL_GROUP.add_argument(
    '--no-validity',
    help='Do not check SSL certificate duration',
    action='store_true'
)
ARGS = OPTIONS.parse_args()

# initiate output and perfdata
OUT = cp_output.CpOutput()
PERF = cp_perfdata.CpPerfdata()
SSL = cp_ssl.CpSSL(ARGS.host, ARGS.port)

# build output
if not ARGS.no_validity:
    OUT.add_short(
        'Certificate expires for \'{}\' in days: {} - Validity Date: {}'.
        format(
            SSL.get_subject(), SSL.get_expiration_from_now(),
            SSL.get_expiration_date()
        )
    )

if ARGS.subject is not None:
    if ARGS.subject == SSL.get_subject():
        OUT.add_short('Certificate subject is valid')
    else:
        OUT.add_short('Invalid subject', status='critical')

if ARGS.issuer is not None:
    if ARGS.issuer == SSL.get_issuer():
        OUT.add_short('Certificate issuer is valid')
    else:
        OUT.add_short('Invalid issuer', status='critical')

OUT.render()
