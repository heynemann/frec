#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

from pyvows import Vows, expect

import frec.recognizers.models as mod
from frec.recognizers.features import AbstractFeature
from frec.recognizers.classifiers import AbstractClassifier

class MockFeature(AbstractFeature):
    def __init__(self, name):
        self.name = name

    def compute(self, x, y):
        return "computed %s %s %s" % (self.name, x, y)

    def extract(self, x):
        return "extracted %s %s" % (self.name, x)

    def __repr__(self):
        return "MockFeature (%s)" % self.name


class MockClassifier(AbstractClassifier):
    def __init__(self, name):
        self.name = name
        self.computed = None

    def compute(self, x, y):
        self.computed = "computed %s %s %s" % (self.name, x, y)

    def predict(self, x):
        return "predicted %s %s" % (self.name, x)

    def __repr__(self):
        return "MockClassifier (%s)" % self.name


@Vows.batch
class PredictableModel(Vows.Context):

    def topic(self):
        return mod.PredictableModel(
            feature=MockFeature("feature"),
            classifier=MockClassifier("classifier")
        )

    def should_be_instance_of(self, topic):
        expect(topic).to_be_instance_of(mod.PredictableModel)

    class WhenCallingCompute(Vows.Context):
        def topic(self, model):
            model.compute(3, 4)
            return model

        def should_be_proper_value(self, topic):
            expect(topic.classifier.computed).to_equal('computed classifier computed feature 3 4 4')

    class WhenCallingPredict(Vows.Context):
        def topic(self, model):
            return model.predict([1, 2, 3, 4])

        def should_be_proper_value(self, topic):
            expect(topic).not_to_be_an_error()
            expect(topic).to_equal('predicted classifier extracted feature [1, 2, 3, 4]')

    class StringRepresentation(Vows.Context):
        def topic(self, feature):
            return str(feature)

        def should_be_abstract_feature(self, topic):
            expect(topic).to_equal('PredictableModel (feature=MockFeature (feature), classifier=MockClassifier (classifier))')

    class WhenInvalidFeature(Vows.Context):

        def topic(self):
            return mod.PredictableModel(
                feature="Invalid Feature",
                classifier=MockClassifier("classifier")
            )

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()
            expect(topic).to_be_an_error_like(TypeError)

    class WhenInvalidClassifier(Vows.Context):

        def topic(self):
            return mod.PredictableModel(
                feature=MockFeature("feature"),
                classifier="Invalid Classifier"
            )

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()
            expect(topic).to_be_an_error_like(TypeError)

