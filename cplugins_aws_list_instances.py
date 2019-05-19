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
import boto3

# define some variables
EC2_INSTANCES_STATUS = {
    'pending': {
        'warning': 0,
        'critical': None
    },
    'running': {
        'warning': None,
        'critical': None
    },
    'shutting-down': {
        'warning': None,
        'critical': 0
    },
    'terminated': {
        'warning': None,
        'critical': 0
    },
    'stopping': {
        'warning': None,
        'critical': 0
    },
    'stopped': {
        'warning': 0,
        'critical': None
    }
}
STATE_SUM = {}
OUT = cp_output.CpOutput()

# define specific command line arguments
OPTIONS = argparse.ArgumentParser(parents=[cp_options.CpOptions().parser])
LOCAL_GROUP = OPTIONS.add_argument_group('Specific options')
LOCAL_GROUP.add_argument('-r', '--region', help='give the aws region')
LOCAL_GROUP.add_argument(
    '-s',
    '--states',
    help='list of states to check; ex: running,stopped,...',
    nargs='+',
    choices=EC2_INSTANCES_STATUS.keys()
)
LOCAL_GROUP.add_argument(
    '-e',
    '--exclude-states',
    help='list of states to exclude from check',
    nargs='+',
    choices=EC2_INSTANCES_STATUS.keys()
)
ARGS = OPTIONS.parse_args()

# initialise the state list to filter on
if ARGS.states is not None:
    STATE_LIST = ARGS.states
else:
    STATE_LIST = EC2_INSTANCES_STATUS.keys()
for state in STATE_LIST:
    STATE_SUM[state] = 0

# initialise instance id
if ARGS.host == 'all':
    INSTANCE_ID = []
else:
    INSTANCE_ID = [ARGS.host]

# request data
EC2 = boto3.resource('ec2', region_name=ARGS.region)
INSTANCES = EC2.instances.filter(
    InstanceIds=INSTANCE_ID,
    Filters=[{
        'Name': 'instance-state-name',
        'Values': STATE_LIST
    }]
)

# will use perfdata
PERF = cp_perfdata.CpPerfdata()

# Sum of instances (total and each states)
TOTAL = 0
for instance in INSTANCES:
    TOTAL += 1
    STATE_SUM[instance.state['Name']] += 1
    OUT.add_long(
        '\'' + instance.id + '\' [state = ' + instance.state['Name'] + ']'
    )

for state in STATE_LIST:
    PERF.add(
        STATE_SUM[state],
        warning=EC2_INSTANCES_STATUS[state]['warning'],
        critical=EC2_INSTANCES_STATUS[state]['critical'],
        perfname=state,
        output=state + ' instances: ' + str(STATE_SUM[state])
    )

PERF.add(TOTAL, perfname='total')
OUT.default_output = 'Total instances: ' + str(TOTAL)
OUT.forced_output = OUT.default_output
OUT.render(PERF)
