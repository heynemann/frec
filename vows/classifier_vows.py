#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

from pyvows import Vows, expect

import frec.recognizers.classifiers as cl


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
