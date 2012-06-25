#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

# code adapted from facerec's models module
# (https://github.com/bytefish/facerec)

from frec.recognizers.features import AbstractFeature
from frec.recognizers.classifiers import AbstractClassifier


class PredictableModel(object):
    def __init__(self, feature, classifier):
        if not isinstance(feature, AbstractFeature):
            raise TypeError("feature must be of type AbstractFeature!")
        if not isinstance(classifier, AbstractClassifier):
            raise TypeError("classifier must be of type AbstractClassifier!")

        self.feature = feature
        self.classifier = classifier

    def compute(self, x, y):
        features = self.feature.compute(x, y)
        self.classifier.compute(features, y)

    def predict(self, x):
        q = self.feature.extract(x)
        return self.classifier.predict(q)

    def __repr__(self):
        feature_repr = repr(self.feature)
        classifier_repr = repr(self.classifier)
        return "PredictableModel (feature=%s, classifier=%s)" % (feature_repr, classifier_repr)
