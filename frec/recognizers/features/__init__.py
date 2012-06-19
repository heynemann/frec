#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

# code adapted from facerec's feature module (https://github.com/bytefish/facerec)

class AbstractFeature(object):

    def compute(self, x, y):
        raise NotImplementedError("Every AbstractFeature must implement the compute method.")

    def extract(self, x, y):
        raise NotImplementedError("Every AbstractFeature must implement the extract method.")

    def __repr__(self):
        return "AbstractFeature"

