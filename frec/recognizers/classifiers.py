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
    def __init__(self, dist_metric=None, k=1):
        AbstractClassifier.__init__(self)

        if dist_metric is None:
            dist_metric = dist.EuclideanDistance()

        self.k = k
        self.dist_metric = dist_metric
        self.x = []
        self.y = []

    def compute(self, x, y):
        self.x.append(x)
        self.y = y

        return self

    def predict(self, photo_to_recognize):
        if len(self.y) == 0:
            return None

        distances = []

        for person in self.x:
            min_person_distance = sys.float_info.max
            for photo in person:
                # why?
                #photo = photo.reshape(-1, 1)

                d = self.dist_metric(photo, photo_to_recognize)
                if d < min_person_distance:
                    min_person_distance = d

            distances.append(min_person_distance)

        if len(distances) > len(self.y):
            raise Exception("More distances than classes. Is your distance metric correct?")

        idx = np.argsort(np.array(distances))

        sorted_y = np.array(self.y)[idx]
        sorted_y = sorted_y[0:self.k]

        bin_count = np.bincount(sorted_y)

        hist = [(key, val) for key, val in enumerate(bin_count) if val]
        hist = dict(hist)

        return max(hist.iteritems(), key=op.itemgetter(1))[0]

    def __repr__(self):
        return "NearestNeighbor (k=%s, dist_metric=%s)" % (self.k, repr(self.dist_metric))
