#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

import os.path as path
from collections import defaultdict

from pyvows import Vows, expect

import frec.recognizers.operators as op
import frec.image as image

ROOT_PATH = path.abspath(path.join(path.dirname(__file__), 'orl_faces'))
image_path = lambda person, picture: path.join(
    ROOT_PATH, 's%d' % person, '%d.pgm' % picture)

test_data = []
for person in range(1, 41):
    for picture in range(1, 10):
        test_data.append((person, picture, image_path(person, picture)))

cache = {}


def _read(path):
    if path in cache:
        return cache[path]
    with open(path, 'rb') as f:
        contents = f.read()
        cache[path] = contents
        return contents


@Vows.batch
class TanTriggsPreProcessing(Vows.Context):
    def topic(self):
        return op.ChainOperator()

    def should_be_instance_of(self, topic):
        expect(topic).to_be_instance_of(op.ChainOperator)

    def should_have_proper_representation(self, topic):
        expect(str(topic)).to_equal('ChainOperator()')

    class WhenPreprocessingImage(Vows.Context):
        def topic(self, pre_processor):
            images = defaultdict(list)
            for data in test_data:
                person, picture, file_path = data
                img = image.Image.create_from_buffer(_read(file_path))
                images[person].append(
                    img.to_array()
                )

            people = []
            images_list = []
            for person, images in images.iteritems():
                people.append(person)
                images_list.append(images)

            return pre_processor.compute(images_list, people)

        def should_not_be_empty(self, topic):
            expect(topic).not_to_be_null()
            expect(topic).not_to_be_an_error()
