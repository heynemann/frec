#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

import os.path as path

from pyvows import Vows, expect

import frec.recognizers.lbp as lbp
import frec.image as image

ROOT_PATH = path.abspath(path.join(path.dirname(__file__), 'orl_faces'))
image_path = lambda person, picture: path.join(ROOT_PATH, 's%d' % person, '%d.pgm' % picture)

test_data = []
for person in range(1, 41):
    for picture in range(1, 10):
        test_data.append(image_path(person, picture))

def _read(path):
    with open(path, 'rb') as f:
        return f.read()

@Vows.batch
class LbpTrainer(Vows.Context):
    class ShouldNotDetectAnythingBeforeTraining(Vows.Context):
        def topic(self):
            for data in test_data:
                file_path, x, y, w, h = data

                img = image.Image.create_from_buffer(_read(file_path))

                recognizer = lbp.LBPRecognizer()
                yield recognizer.recognize(img)

        def should_be_empty_dict(self, topic):
            expect(topic).to_be_empty()

