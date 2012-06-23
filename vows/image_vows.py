#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

import os.path as path
from pyvows import Vows, expect

import frec.image as image

IMAGE_PATH = path.abspath(
    path.join(path.dirname(__file__), 'fixtures', 'image.jpg')
)


@Vows.batch
class ImageModule(Vows.Context):

    class FromBuffer(Vows.Context):
        def topic(self):
            with open(IMAGE_PATH, 'r') as img:
                data = img.read()

            return image.Image.create_from_buffer(data)

        def should_have_image_property(self, topic):
            expect(topic.image).not_to_be_null()

        def should_have_proper_size(self, topic):
            expect(topic.size[0]).to_equal(300)
            expect(topic.size[1]).to_equal(130)

        def should_have_proper_channels(self, topic):
            expect(topic.color_channels).to_equal(3)

        class GreyImage(Vows.Context):
            def topic(self, img):
                img.grayscale()
                return img

            def should_have_image_property(self, topic):
                expect(topic.image).not_to_be_null()

            def should_have_proper_size(self, topic):
                expect(topic.size[0]).to_equal(300)
                expect(topic.size[1]).to_equal(130)

            def should_have_proper_channels(self, topic):
                expect(topic.color_channels).to_equal(1)

    class FromInvalidBuffer(Vows.Context):
        def topic(self):
            return image.Image.create_from_buffer('not')

        def should_be_null(self, topic):
            expect(topic).to_be_null()

    class ValidImage(Vows.Context):
        def topic(self):
            with open(IMAGE_PATH, 'r') as img:
                data = img.read()

            img = image.Image.create_from_buffer(data)
            return img.is_valid(data)

        def should_be_true(self, topic):
            expect(topic).to_be_true()
