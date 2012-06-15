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

IMAGE_PATH = path.abspath(path.join(path.dirname(__file__), 'fixtures', 'image.jpg'))

@Vows.batch
class ImageModule(Vows.Context):
    class FromBuffer(Vows.Context):
        def topic(self):
            with open(IMAGE_PATH, 'r') as img:
                data = img.read()

            return image.Image.create_from_buffer(data)

        def should_have_image_property(self, topic):
            expect(topic.image).not_to_be_null()
