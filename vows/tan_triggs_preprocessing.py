#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

from pyvows import Vows, expect

import frec.recognizers.pre_processing.tan_triggs as proc

@Vows.batch
class TanTriggsPreProcessing(Vows.Context):
    def topic(self):
        return proc.TanTriggsPreProcessing()

    def should_be_instance_of(self, topic):
        expect(topic).to_be_instance_of(proc.TanTriggsPreProcessing)


