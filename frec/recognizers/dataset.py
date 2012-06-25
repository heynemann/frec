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

import numpy as np

import frec.image as im

class DataSet(object):
    def __init__(self, size=(130, 130)):
        self.data = defaultdict(list)
        self.size = size

    def train(self, label, images):
        for image in images:
            img = im.Image.create_from_buffer(image).resize(self.size)

            self.data[label].append(np.asarray(img.to_array(), dtype=np.uint8))


