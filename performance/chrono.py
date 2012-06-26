#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

import time

class Chrono:

    def __init__(self, name):
        self.name = name
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    @property
    def ellapsed(self):
        if not self.end_time:
            return 0

        return self.end_time - self.start_time

    def __repr__(self):
        return 'Chronograph %s, ellapsed: %ss' % (self.name, self.ellapsed)

