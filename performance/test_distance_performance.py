#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

import os.path as path

import chrono as ch
from frec.recognizers.distance import ChiSquareDistance, EuclideanDistance
from frec.image import Image

ROOT_PATH = path.abspath(path.dirname(__file__))
image_path = lambda person: path.join(
    ROOT_PATH, '%d.pgm' % person
)

cache = {}
def _read(path):
    if path in cache:
        return cache[path]
    with open(path, 'rb') as f:
        contents = f.read()
        cache[path] = contents
        return contents

PATH1 = image_path(1)
PATH2 = image_path(2)
IMG1 = Image.create_from_buffer(_read(PATH1)).grayscale().to_array()
IMG2 = Image.create_from_buffer(_read(PATH2)).grayscale().to_array()

def test(iterations=1000):
    euclidean_timer = ch.Chrono('euclidean')
    chi_timer = ch.Chrono('chiSquare')

    distance = EuclideanDistance()
    euclidean_timer.start()
    for i in range(iterations):
        distance(IMG1, IMG2)
    euclidean_timer.stop()

    distance = ChiSquareDistance()
    chi_timer.start()
    for i in range(iterations):
        distance(IMG1, IMG2)
    chi_timer.stop()

    print euclidean_timer
    print 'Euclidean: %.2f ops/s' % (float(iterations) / euclidean_timer.ellapsed)

    print chi_timer
    print 'ChiSquare: %.2f ops/s' % (float(iterations) / chi_timer.ellapsed)

if __name__ == '__main__':
    test(10000)
