#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2011 bernardo heynemann heynemann@gmail.com

import os.path as path

from pyvows import Vows, expect

import frec.image as image
import frec.detectors.sync_detector as detector

ROOT_PATH = path.abspath(path.join(path.dirname(__file__), 'orl_faces'))
test_data = (
    path.join(ROOT_PATH, 's1', '1.pgm'),
)

def _read(path):
    with open(path, 'rb') as f:
        return f.read()

@Vows.batch
class SyncDetector(Vows.Context):
    class ShouldReturnDetectedItemsInPicture(Vows.Context):
        def topic(self):
            for data in test_data:
                img = image.Image.create_from_buffer(_read(data))
                det = detector.CascadedDetector(min_neighbors=3, scale_factor=1.1, min_size=(20,20))
                yield det.detect(img.to_array())

        def should_not_be_none(self, topic):
            expect(topic).not_to_be_null()

