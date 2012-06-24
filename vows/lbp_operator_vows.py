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

import frec.recognizers.features.operators as op
import frec.image as image

ROOT_PATH = path.abspath(path.join(path.dirname(__file__), 'orl_faces'))
image_path = lambda person, picture: path.join(
    ROOT_PATH, 's%d' % person, '%d.pgm' % picture
)

test_data = []
for person in range(1, 3):
    for picture in range(1, 3):
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
class LBPOperator(Vows.Context):
    def topic(self):
        return op.LBPOperator(10)

    def should_be_instance_of(self, topic):
        expect(topic).to_be_instance_of(op.LBPOperator)

    def should_have_proper_representation(self, topic):
        expect(str(topic)).to_equal('LBPOperator (neighbors=10)')

    def should_have_proper_neighbors(self, topic):
        expect(topic.neighbors).to_equal(10)

    class UponCalling(Vows.Context):
        def topic(self, operator):
            return operator(10)

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()
            expect(topic).to_be_an_error_like(NotImplementedError)


@Vows.batch
class ExtendedLBPOperator(Vows.Context):
    def topic(self):
        return op.ExtendedLBP()

    def should_be_instance_of(self, topic):
        expect(topic).to_be_instance_of(op.ExtendedLBP)

    def should_have_proper_representation(self, topic):
        expect(str(topic)).to_equal('ExtendedLBP (neighbors=8, radius=1)')

    def should_have_default_radius(self, topic):
        expect(topic.radius).to_equal(1)

    class WhenPreprocessingImage(Vows.Context):
        def topic(self, operator):
            for data in test_data:
                person, picture, file_path = data
                img = image.Image.create_from_buffer(_read(file_path))
                img.grayscale()

                yield operator(img.to_array())

        def should_not_be_empty(self, topic):
            expect(topic).not_to_be_null()
            expect(topic).not_to_be_empty()


@Vows.batch
class LBP(Vows.Context):
    def topic(self):
        return op.LBP()

    def should_be_instance_of(self, topic):
        expect(topic).to_be_instance_of(op.LBP)

    def should_have_proper_representation(self, topic):
        expect(str(topic)).to_equal('Local Binary Pattern (operator=ExtendedLBP (neighbors=8, radius=1), grid=(8, 8))')

    def should_have_default_lbp_operator(self, topic):
        expect(topic.lbp_operator).to_be_instance_of(op.ExtendedLBP)

    def should_have_default_size(self, topic):
        expect(topic.size).to_equal((8, 8))

    class WithInvalidOperator(Vows.Context):
        def topic(self):
            return op.LBP(lbp_operator="INVALID OPERATOR")

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()
            expect(topic).to_be_an_error_like(TypeError)

    class WhenComputingAndExtractingData(Vows.Context):
        def topic(self, feature):
            images = defaultdict(list)
            for data in test_data:
                person, picture, file_path = data
                img = image.Image.create_from_buffer(_read(file_path))
                images[person].append(img.grayscale().to_array())

            people = []
            images_list = []
            for person, images in images.iteritems():
                people.append(person)
                for person_image in images:
                    images_list.append(person_image)

            return feature.compute(images_list, people)

        def should_not_be_an_error(self, topic):
            expect(topic).not_to_be_an_error()
