#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

from pyvows import Vows, expect

import frec.recognizers.features.operators as op

@Vows.batch
class LBPOperator(Vows.Context):
    def topic(self):
        return op.LBPOperator(10)

    def should_be_instance_of(self, topic):
        expect(topic).to_be_instance_of(op.LBPOperator)

    def should_have_proper_representation(self, topic):
        expect(str(topic)).to_equal('LBPOperator (neighbors=10)')

    def should_have_proper_neighbors(self, topic):
        expect(topic.neighbors).to_equal(10)

    class UponCalling(Vows.Context):
        def topic(self, operator):
            return operator(10)

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()
            expect(topic).to_be_an_error_like(NotImplementedError)
