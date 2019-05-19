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
from cplugins import cp_output, cp_perfdata, cp_options

# import specific modules
# put here the import neede by your plugin
# ex: import boto3

# define some specific variables to your plugin
# ex: EC2_instances_status = {
#     'pending': {
#         'warning': 0,
#         'critical': None
#     },
#     'running': {
#         'warning': None,
#         'critical': None
#     },
#     'shutting-down': {
#         'warning': None,
#         'critical': 0
#     },
#     'terminated': {
#         'warning': None,
#         'critical': 0
#     },
#     'stopping': {
#         'warning': None,
#         'critical': 0
#     },
#     'stopped': {
#         'warning': 0,
#         'critical': None
#     }
# }
# state_sum = {}

# initialize the output module
OUT = cp_output.CpOutput()
# initialize perfdata module if needed
# perf = cplugins.CpPerfdata()

# define specific command line arguments
# use the default parser as parent parser
OPTIONS = argparse.ArgumentParser(parents=[cp_options.CpOptions().parser])
# define a local group of arguments
LOCAL_GROUP = OPTIONS.add_argument_group('Specific options')
# ex: local_group.add_argument('-r', '--region', help='give the aws region')
# parse arguments
ARGS = OPTIONS.parse_args()

# put your code here
################################################

################################################

# add some perfdata
# ex: perf.add(state_sum[state], warning=EC2_instances_status[state]['warning'], critical=EC2_instances_status[state]['critical'], perfname=state, output=state + ' instances: ' + str(state_sum[state]))

# change output text if needed
# ex: out.default_output = 'Total instances: ' + str(total)
# ex: out.forced_output = out.default_output

# render and exit
OUT.render()
# render perfdata
# out.render(perf)
