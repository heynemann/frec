#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

# code adapted from remotecv's image module (http://github.com/globocom/remotecv)

import cv

class Image:
    @classmethod
    def create_from_buffer(cls, image_buffer):
        instance = cls()

        if not instance.is_valid(image_buffer):
            return None

        instance.set_image_buffer(image_buffer)
        return instance

    def is_valid(self, image_buffer):
        return len(image_buffer) > 4 and image_buffer[:4] != 'GIF8'

    def set_image_buffer(self, image_buffer):
        buffer_len = len(image_buffer)
        imagefiledata = cv.CreateMatHeader(1, buffer_len, cv.CV_8UC1)
        cv.SetData(imagefiledata, image_buffer, buffer_len)
        self.image = cv.DecodeImage(imagefiledata, cv.CV_LOAD_IMAGE_COLOR)
        self.size = cv.GetSize(self.image)
        self.mode = "BGR"

    def grayscale(self):
        convert_mode = getattr(cv, 'CV_%s2GRAY' % self.mode)

        gray = cv.CreateImage(self.size, cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(self.image, gray, convert_mode)
        cv.EqualizeHist(gray, gray)
        self.image = gray

