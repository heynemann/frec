#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

from pyvows import Vows, expect

import frec.recognizers.distance as ds


@Vows.batch
class AbstractDistance(Vows.Context):
    def topic(self):
        return ds.AbstractDistance('test')

    def should_be_instance_of(self, topic):
        expect(topic).to_be_instance_of(ds.AbstractDistance)

    def should_have_name(self, topic):
        expect(topic.name).to_equal('test')

    def should_have_repr(self, topic):
        expect(str(topic)).to_equal('test')

    class WhenCalling(Vows.Context):
        def topic(self, distance):
            return distance(1, 2)

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()
            expect(topic).to_be_an_error_like(NotImplementedError)


@Vows.batch
class EuclideanDistance(Vows.Context):
    def topic(self):
        return ds.EuclideanDistance()

    def should_have_name(self, topic):
        expect(topic.name).to_equal('EuclideanDistance')

    class WhenComputingDistanceBetweenTwoPoints(Vows.Context):
        def topic(self, distance):
            p = [1, 2, 3, 4]
            q = [2, 3, 4, 5]

            return distance(p, q)

        def should_be_2(self, topic):
            expect(topic).to_equal(2.0)
