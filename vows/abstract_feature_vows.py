#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

from pyvows import Vows, expect

import frec.recognizers.features as features

@Vows.batch
class AbstractFeature(Vows.Context):
    def topic(self):
        return features.AbstractFeature()

    def should_be_instance_of(self, topic):
        expect(topic).to_be_instance_of(features.AbstractFeature)

    class WhenCallingCompute(Vows.Context):
        def topic(self, feature):
            return feature.compute(1, 1)

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()
            expect(topic).to_be_an_error_like(NotImplementedError)


    class WhenCallingExtract(Vows.Context):
        def topic(self, feature):
            return feature.extract(1, 1)

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()
            expect(topic).to_be_an_error_like(NotImplementedError)


    class StringRepresentation(Vows.Context):
        def topic(self, feature):
            return str(feature)

        def should_be_abstract_feature(self, topic):
            expect(topic).to_equal('AbstractFeature')


