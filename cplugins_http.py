#!/usr/bin/env python3
"""Check response time and size of a website."""
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
import sys
import requests
import urllib3
from cplugins import cp_output, cp_perfdata, cp_options

# define specific command line arguments
OPTIONS = argparse.ArgumentParser(parents=[cp_options.CpOptions().parser])
LOCAL_GROUP = OPTIONS.add_argument_group('Specific options')
LOCAL_GROUP.add_argument(
    '-p', '--port', help='Port to connect.', default='443'
)
LOCAL_GROUP.add_argument(
    '--protocol', help='Scheme used to connect.', default='https'
)
LOCAL_GROUP.add_argument(
    '--size', help='Return response size (bytes)', action='store_true'
)
LOCAL_GROUP.add_argument('--size-info', help='unit,warn,crit,min,max')
LOCAL_GROUP.add_argument(
    '--notime', help='Don\'t return response time', action='store_true'
)
LOCAL_GROUP.add_argument('--time-info', help='unit,warn,crit,min,max')
LOCAL_GROUP.add_argument(
    '--skip-verify',
    help='Skip certificate verification',
    action='store_false'
)
LOCAL_GROUP.add_argument(
    '--uri', help='Specific URI to request. Must start with "/".', default='/'
)
ARGS = OPTIONS.parse_args()

# initiate output and perfdata
OUT = cp_output.CpOutput()
PERF = cp_perfdata.CpPerfdata()

# compute full URL
URL = ARGS.protocol + '://' + ARGS.host + ':' + ARGS.port + ARGS.uri

if not ARGS.skip_verify:
    urllib3.disable_warnings()
# get data
try:
    F = requests.get(URL, verify=ARGS.skip_verify)
    RESPONSE_TIME = F.elapsed.total_seconds()
    RESPONSE_SIZE = sys.getsizeof(F.content)
    RESPONSE_CODE = F.status_code
except requests.exceptions.ConnectionError:
    RESPONSE_CODE = 500

# build output
if RESPONSE_CODE == 200:
    if not ARGS.notime:
        PERF.add(RESPONSE_TIME, perfname='time', unit='s', info=ARGS.time_info)
    if ARGS.size:
        PERF.add(RESPONSE_SIZE, perfname='size', unit='b', info=ARGS.size_info)
    OUT.add_short('Connection OK')
    OUT.render(PERF)
else:
    OUT.add_short(
        'Error connecting to URL: {} [return code: {}]'.format(
            URL, RESPONSE_CODE
        ),
        status='critical'
    )
    OUT.render()
