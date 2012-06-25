#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

from pyvows import Vows, expect

import frec.recognizers.classifiers as cl
import frec.recognizers.distance as dist


@Vows.batch
class AbstractClassifier(Vows.Context):
    def topic(self):
        return cl.AbstractClassifier()

    def should_be_instance_of(self, topic):
        expect(topic).to_be_instance_of(cl.AbstractClassifier)

    class OnCompute(Vows.Context):
        def topic(self, classifier):
            return classifier.compute(1, 2)

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()
            expect(topic).to_be_an_error_like(NotImplementedError)

    class OnPredict(Vows.Context):
        def topic(self, classifier):
            return classifier.predict(1)

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()
            expect(topic).to_be_an_error_like(NotImplementedError)


@Vows.batch
class NearestNeighbor(Vows.Context):
    def topic(self):
        return cl.NearestNeighbor()

    def should_have_euclidean_distance(self, topic):
        expect(topic.dist_metric).to_be_instance_of(dist.EuclideanDistance)

    def should_have_k_equal_1(self, topic):
        expect(topic.k).to_equal(1)

    def should_have_proper_representation(self, topic):
        expect(str(topic)).to_equal(
            'NearestNeighbor (k=1, dist_metric=EuclideanDistance)')

    class WhenComputing(Vows.Context):
        def topic(self, classifier):
            return classifier.compute(1, 2)

        def should_keep_first_value_as_x(self, topic):
            expect(topic.x).to_equal([1])

        def should_keep_second_value_as_y(self, topic):
            expect(topic.y).to_equal(2)
