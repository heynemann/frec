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
from frec.recognizers.features import AbstractFeature

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


class MockFeature(AbstractFeature):
    def __init__(self, name):
        self.name = name

    def compute(self, x, y):
        return "Mock compute %s %s %s" % (self.name, x, y)

    def extract(self, x):
        return "Mock extract %s %s" % (self.name, x)

    def __repr__(self):
        return "MockOperator %s" % self.name


@Vows.batch
class ChainOperator(Vows.Context):
    def topic(self):
        return op.ChainOperator(MockFeature('1'), MockFeature('2'))

    def should_be_instance_of(self, topic):
        expect(topic).to_be_instance_of(op.ChainOperator)

    def should_have_proper_representation(self, topic):
        expect(str(topic)) \
            .to_equal('ChainOperator(MockOperator 1,MockOperator 2)')

    class WhenExtractCalled(Vows.Context):
        def topic(self, operator):
            return operator.extract("something")

        def should_run_both_extractors(self, topic):
            expect(topic).to_equal('Mock extract 2 Mock extract 1 something')

    class WhenComputeCalled(Vows.Context):
        def topic(self, operator):
            return operator.compute("something1", "something2")

        def should_run_both_computes(self, topic):
            expect(topic).to_equal('Mock compute 2 Mock compute 1 something1 something2 something2')
