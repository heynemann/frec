#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2012 Bernardo Heynemann heynemann@gmail.com

# code adapted from remotecv's image module
# (http://github.com/globocom/remotecv)

import cv2
import numpy as np


class Image:
    @classmethod
    def create_from_buffer(cls, image_buffer):
        if isinstance(image_buffer, Image):
            return image_buffer

        instance = cls()

        if not instance.is_valid(image_buffer):
            return None

        instance.set_image_buffer(image_buffer)
        return instance

    @property
    def size(self):
        return (self.image.shape[1], self.image.shape[0])

    @property
    def color_channels(self):
        if len(self.image.shape) > 2:
            return self.image.shape[2]

        return 1

    def is_valid(self, image_buffer):
        return len(image_buffer) > 4 and image_buffer[:4] != 'GIF8'

    def set_image_buffer(self, image_buffer):
        self.mode = "BGR"
        buffer_array = np.fromstring(image_buffer, dtype=np.uint8)
        self.image = cv2.imdecode(buffer_array, 1)

    def grayscale(self):
        convert_mode = getattr(cv2, 'COLOR_%s2GRAY' % self.mode)
        self.image = cv2.cvtColor(self.image, convert_mode)
        self.image = cv2.equalizeHist(self.image)
        return self

    def resize(self, size):
        self.image = cv2.resize(self.image, size)
        return self

    def to_array(self):
        return np.array(self.image, dtype=np.uint8)

    def save(self, path):
        cv2.imwrite(path, self.image)
