#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

# code adapted from facerec's distance module
# (https://github.com/bytefish/facerec)

import numpy as np


class AbstractDistance(object):
    def __init__(self, name):
        self._name = name

    def __call__(self, p, q):
        raise NotImplementedError(
            "Every AbstractDistance must implement the __call__ method.")

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return self._name


class EuclideanDistance(AbstractDistance):
    def __init__(self):
        AbstractDistance.__init__(self, "EuclideanDistance")

    def __call__(self, p, q):
        p = np.asarray(p).flatten()
        q = np.asarray(q).flatten()
        return np.sqrt(np.sum(np.power((p - q), 2)))


class ChiSquareDistance(AbstractDistance):
    """
        Negated Mahalanobis Cosine Distance.

        Literature:
            "Studies on sensitivity of face recognition performance to eye location accuracy.". Master Thesis (2004), Wang
    """
    def __init__(self):
        AbstractDistance.__init__(self, "ChiSquareDistance")

    def __call__(self, p, q):
        p = np.asarray(p).flatten()
        q = np.asarray(q).flatten()

        bin_dists = (p - q) ** 2 / (p + q + np.finfo('float').eps)
        return np.sum(bin_dists)
