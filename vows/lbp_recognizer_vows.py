#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

from collections import defaultdict
import os.path as path

from pyvows import Vows, expect

import frec.recognizers.lbp as lbp
import frec.image as image

ROOT_PATH = path.abspath(path.join(path.dirname(__file__), 'orl_faces'))
image_path = lambda person, picture: path.join(
    ROOT_PATH, 's%d' % person, '%d.pgm' % picture
)

test_data = []
for person in range(1, 41):
    for picture in range(1, 11):
        test_data.append((person, picture, image_path(person, picture)))

half_test_data = []
for person in range(1, 21):
    for picture in range(1, 11):
        half_test_data.append((person, picture, image_path(person, picture)))

cache = {}


def _read(path):
    if path in cache:
        return cache[path]
    with open(path, 'rb') as f:
        contents = f.read()
        cache[path] = contents
        return contents


@Vows.batch
class LbpRecognizer(Vows.Context):
    class ShouldNotDetectAnythingBeforeTraining(Vows.Context):
        def topic(self):
            for data in test_data:
                person, picture, file_path = data
                img = image.Image.create_from_buffer(_read(file_path))
                recognizer = lbp.Recognizer()
                yield (recognizer, recognizer.recognize(img))

        def should_be_null(self, (recognizer, topic)):
            expect(topic).to_be_null()

    class AfterTrainingHalf(Vows.Context):
        def topic(self):
            recognizer = lbp.Recognizer()

            people = defaultdict(list)
            for data in half_test_data:
                person, picture, file_path = data
                img = image.Image.create_from_buffer(_read(file_path))
                people[person].append(img)

            for person in people.keys():
                recognizer.train(person, people[person])

            recognizer.compute()

            for data in half_test_data:
                person, picture, file_path = data
                if picture > 1: continue
                img = image.Image.create_from_buffer(_read(file_path))
                yield (recognizer, person, picture, recognizer.recognize(img))


        def should_be_right(self, (recognizer, person, picture, topic)):
            expect(topic).to_equal(person)

