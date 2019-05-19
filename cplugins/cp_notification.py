# -*- coding: utf-8 -*-
# from .cp_debug import CpDebug
# from pydoc import locate
import json
import argparse
from .cp_options import CpOptions
from .notifications import cp_email


class CpNotification():
    def __init__(self, notif_type, args=None):
        self.notif_type = notif_type
        self.conf = json.loads('{}')
        self.args = args
        self.macros = {
            '0': 'host_name',
            '1': 'host_state',
            '2': 'host_output',
            '3': 'host_ack_author',
            '4': 'host_ack_comment',
            '5': 'service_desc',
            '6': 'service_state',
            '7': 'service_output',
            '8': 'service_ack_author',
            '9': 'service_ack_comment',
            '10': 'notification_type',
            '11': 'long_date_time'
        }
        if args is not None:

            # load conf file
            try:
                file = open(args.config_notifications)
            except IOError as e:
                print(e)
            else:
                with file:
                    self.conf = json.load(file)
            self.parse_params()

            if self.args.parameters['service_state'] is '':
                self.args.parameters['object_name'
                                     ] = self.args.parameters['host_name']
                self.args.parameters['state'] = self.args.parameters[
                    'host_state'].upper()
                self.args.parameters['ack_author'] = self.args.parameters[
                    'host_ack_author']
                self.args.parameters['ack_comment'] = self.args.parameters[
                    'host_ack_comment']
                self.args.parameters['output'
                                     ] = self.args.parameters['host_output']
            else:
                self.args.parameters['object_name'] = self.args.parameters[
                    'host_name'] + '/' + self.args.parameters['service_desc']
                self.args.parameters['state'] = self.args.parameters[
                    'service_state'].upper()
                self.args.parameters['ack_author'] = self.args.parameters[
                    'service_ack_author']
                self.args.parameters['ack_comment'] = self.args.parameters[
                    'service_ack_comment']
                self.args.parameters['output'
                                     ] = self.args.parameters['service_output']

    def sendEmail(self):
        cp_email.CpEmail(self.conf, self.args)

    def parse_params(self):
        '''parse parameters given, must be always in the same order...'''
        macro_values = {}
        for key, value in self.macros.items():
            macro_values[value] = self.args.parameters[int(key)]
        self.args.parameters = macro_values
