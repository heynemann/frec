#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

# code adapted from facerec's detector module (https://github.com/bytefish/facerec)

import os.path as path
import os

import cv2
import numpy as np

import frec.face as face

class Detector:
    def detect(self, src):
        raise NotImplementedError("Every Detector must implement the detect method.")

class CascadedDetector(Detector):
    """
    Uses the OpenCV cascades to perform the detection. Returns the Regions of Interest, where
    the detector assumes a face. You probably have to play around with the scale_factor,
    min_neighbors and min_size parameters to get good results for your use case. From my
    personal experience, all I can say is: there's no parameter combination which *just
    works*.
    """
    def __init__(self, cascade_file=None, scale_factor=1.2, min_neighbors=5, min_size=(30,30)):
        if cascade_file is None:
            cascade_file = path.abspath(path.join(path.dirname(__file__), 'cascades', 'haarcascade_frontalface_alt2.xml'))
        if not os.path.exists(cascade_file):
            raise IOError("No valid cascade found for path=%s." % cascade_file)
        self.cascade = cv2.CascadeClassifier(cascade_file)
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size

    def detect(self, src):
        if np.ndim(src) == 3:
            src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        src = cv2.equalizeHist(src)
        rects = self.cascade.detectMultiScale(src, scaleFactor=self.scale_factor, minNeighbors=self.min_neighbors, minSize=self.min_size)
        if len(rects) == 0:
            return []

        faces = []
        for rect in rects.tolist():
            if len(rect) != 4: continue
            faces.append(face.Face(x=rect[0], y=rect[1], width=rect[2], height=rect[3]))
        return faces
