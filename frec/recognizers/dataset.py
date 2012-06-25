#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

# code adapted from facerec's dataset module
# (https://github.com/bytefish/facerec)

from collections import defaultdict


class DataSet(object):
    def __init__(self, size=(130, 130)):
        self.data = defaultdict(list)
        self.size = size

    def train(self, label, images):
        for image in images:
            image.grayscale()
            self.data[label].append(image.to_array())
