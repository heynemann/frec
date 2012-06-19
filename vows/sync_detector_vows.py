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
image_path = lambda person, picture: path.join(ROOT_PATH, 's%d' % person, '%d.pgm' % picture)
test_data = [
    (image_path(1, 1), 9, 29, 74, 74),
    (image_path(1, 3), 7, 24, 74, 74),
]

not_found = [
    image_path(1, 2),
]

def _read(path):
    with open(path, 'rb') as f:
        return f.read()

@Vows.batch
class SyncDetector(Vows.Context):
    class ShouldReturnDetectedItemsInPicture(Vows.Context):
        def topic(self):
            for data in test_data:
                file_path, x, y, w, h = data

                img = image.Image.create_from_buffer(_read(file_path))
                det = detector.CascadedDetector(min_neighbors=5, scale_factor=1.1, min_size=(20,20))
                yield (det.detect(img.to_array()), x, y, w, h)

        def should_not_be_none(self, (topic, x, y, w, h)):
            expect(topic).not_to_be_null()

        def should_not_be_empty(self, (topic, x, y, w, h)):
            expect(topic).not_to_be_empty()

        def should_have_found_one_face(self, (topic, x, y, w, h)):
            expect(topic).to_length(1)

        def should_have_proper_dimensions(self, (topic, x, y, w, h)):
            expect(topic[0].x).to_equal(x)
            expect(topic[0].y).to_equal(y)
            expect(topic[0].width).to_equal(w)
            expect(topic[0].height).to_equal(h)

