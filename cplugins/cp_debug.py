# -*- coding: utf-8 -*-
import logging
from .cp_options import CpOptions


class CpDebug():
    def __init__(self):
        self.args = CpOptions().parser.parse_args()
        self.debug = logging.getLogger('debug')
        debug = logging.StreamHandler()
        debug.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        debug.setFormatter(formatter)
        self.debug.addHandler(debug)
        if self.args.log:
            self.debug.addHandler(self.log())

    def log(self):
        log = logging.FileHandler(self.args.log)
        log.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        log.setFormatter(formatter)
        return log
