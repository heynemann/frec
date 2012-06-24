#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

# code adapted from facerec's classifier module
# (https://github.com/bytefish/facerec)


class AbstractClassifier(object):
    def compute(self, x, y):
        msg = "Every AbstractClassifier must implement the compute method."
        raise NotImplementedError(msg)

    def predict(self, x):
        msg = "Every AbstractClassifier must implement the predict method."
        raise NotImplementedError(msg)
