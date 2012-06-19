#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

# code adapted from facerec's preprocessing module (https://github.com/bytefish/facerec)

import numpy as np
from scipy import ndimage

from frec.recognizers.features import AbstractFeature

class TanTriggsPreProcessing(AbstractFeature):
    def __init__(self, alpha = 0.1, tau = 10.0, gamma = 0.2, sigma0 = 1.0, sigma1 = 2.0):
        AbstractFeature.__init__(self)
        self.alpha = float(alpha)
        self.tau = float(tau)
        self.gamma = float(gamma)
        self.sigma0 = float(sigma0)
        self.sigma1 = float(sigma1)

    def compute(self, x, y):
        xp = []
        for xi in x:
            xp.append(self.extract(xi))
        return xp

    def extract(self, x):
        x = np.array(x, dtype=np.float32)
        x = np.power(x, self.gamma)
        x = np.asarray(ndimage.gaussian_filter(x, self.sigma1) - ndimage.gaussian_filter(x, self.sigma0))
        x = x / np.power(np.mean(np.power(np.abs(x), self.alpha)), 1.0 / self.alpha)
        x = x / np.power(np.mean(np.power(np.minimum(np.abs(x), self.tau), self.alpha)), 1.0 / self.alpha)
        x = self.tau * np.tanh(x / self.tau)
        return x

    def __repr__(self):
        return "TanTriggsPreprocessing (alpha=%.3f,tau=%.3f,gamma=%.3f,sigma0=%.3f,sigma1=%.3f)" % (
            self.alpha,
            self.tau,
            self.gamma,
            self.sigma0,
            self.sigma1
        )

