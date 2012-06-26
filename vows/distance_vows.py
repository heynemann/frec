#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

import numpy as np
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
            return distance(np.array([1]), np.array([2]))

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
            p = np.array([1, 2, 3, 4])
            q = np.array([2, 3, 4, 5])

            return distance(p, q)

        def should_be_2(self, topic):
            expect(topic).to_equal(2.0)


@Vows.batch
class ChiSquareDistance(Vows.Context):
    def topic(self):
        return ds.ChiSquareDistance()

    def should_have_name(self, topic):
        expect(topic.name).to_equal('ChiSquareDistance')

    class WhenComputing(Vows.Context):
        def topic(self, distance):
            p = np.array([1.0, 2.0, 3.0, 4.0])
            q = np.array([2.0, 3.0, 4.0, 5.0])

            return distance(p, q)

        def should_have_proper_value(self, topic):
            expect(round(topic, 4)).to_equal(0.7873)

