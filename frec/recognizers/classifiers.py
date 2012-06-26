#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

# code adapted from facerec's classifier module
# (https://github.com/bytefish/facerec)

import sys

import numpy as np
import operator as op

import frec.recognizers.distance as dist


class AbstractClassifier(object):
    def compute(self, x, y):
        msg = "Every AbstractClassifier must implement the compute method."
        raise NotImplementedError(msg)

    def predict(self, x):
        msg = "Every AbstractClassifier must implement the predict method."
        raise NotImplementedError(msg)


class NearestNeighbor(AbstractClassifier):
    """
    Implements a k-Nearest Neighbor Model for a generic distance metric.
    """
    def __init__(self, dist_metric=None, k=1, max_items=5):
        AbstractClassifier.__init__(self)

        if dist_metric is None:
            dist_metric = dist.EuclideanDistance()

        self.k = k
        self.max_items = 5
        self.dist_metric = dist_metric
        self.x = []
        self.y = []

    def compute(self, x, y):
        self.x.append(x)
        self.y = y

        return self

    def predict(self, feature_to_recognize):
        if len(self.y) == 0:
            return None

        distances = []

        for person in self.x:
            min_distance = 100000000000
            for feature in person:
                d = self.dist_metric(feature, feature_to_recognize)
                if d < min_distance:
                    min_distance = d

            distances.append(min_distance)

        if len(distances) > len(self.y):
            raise Exception("More distances than classes. Is your distance metric correct?")

        result = []
        for i, distance in enumerate(distances):
            result.append((self.y[i], distance))

        result = sorted(result, key=lambda (label, distance): distance)

        return result[:self.max_items]


    def __repr__(self):
        return "NearestNeighbor (k=%s, dist_metric=%s)" % (self.k, repr(self.dist_metric))

