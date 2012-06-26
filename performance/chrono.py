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
        self.iterations = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def iterate(self):
        self.iterations += 1

    @property
    def ellapsed(self):
        if not self.end_time:
            return 0

        return self.end_time - self.start_time

    @property
    def speed(self):
        return (float(self.iterations) / self.ellapsed)

    def __repr__(self):
        return 'Chronograph %s, ellapsed: %ss\n%s: %.2f ops/s' % (self.name, self.ellapsed, self.name, self.speed)

