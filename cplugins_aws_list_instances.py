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
import argparse
from cplugins import cp_output, cp_perfdata, cp_options

# import specific modules
import boto3

# define some variables
EC2_instances_status = {
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
state_sum = {}
out = cp_output.CpOutput()

# define specific command line arguments
options = argparse.ArgumentParser(parents=[cp_options.CpOptions().parser])
local_group = options.add_argument_group('Specific options')
local_group.add_argument('-r', '--region', help='give the aws region')
local_group.add_argument(
    '-s',
    '--states',
    help='list of states to check; ex: running,stopped,...',
    nargs='+',
    choices=EC2_instances_status.keys()
)
local_group.add_argument(
    '-e',
    '--exclude-states',
    help='list of states to exclude from check',
    nargs='+',
    choices=EC2_instances_status.keys()
)
args = options.parse_args()

# initialise the state list to filter on
if args.states is not None:
    state_list = args.states
else:
    state_list = EC2_instances_status.keys()
for state in state_list:
    state_sum[state] = 0

# initialise instance id
if args.host == 'all':
    instance_id = []
else:
    instance_id = [args.host]

# request data
ec2 = boto3.resource('ec2', region_name=args.region)
instances = ec2.instances.filter(
    InstanceIds=instance_id,
    Filters=[{
        'Name': 'instance-state-name',
        'Values': state_list
    }]
)

# will use perfdata
perf = cp_perfdata.CpPerfdata()

# Sum of instances (total and each states)
total = 0
for instance in instances:
    total += 1
    state_sum[instance.state['Name']] += 1
    out.add_long(
        '\'' + instance.id + '\' [state = ' + instance.state['Name'] + ']'
    )

for state in state_list:
    perf.add(
        state_sum[state],
        warning=EC2_instances_status[state]['warning'],
        critical=EC2_instances_status[state]['critical'],
        perfname=state,
        output=state + ' instances: ' + str(state_sum[state])
    )

perf.add(total, perfname='total')
out.default_output = 'Total instances: ' + str(total)
out.forced_output = out.default_output
out.render(perf)
