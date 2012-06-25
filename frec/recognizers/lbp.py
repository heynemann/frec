#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

import numpy as np

from frec.recognizers.features.operators import ChainOperator
from frec.recognizers.pre_processing.tan_triggs import TanTriggsPreProcessing
from frec.recognizers.features.operators import LBP
from frec.recognizers.classifiers import NearestNeighbor
from frec.recognizers.distance import ChiSquareDistance
from frec.recognizers.models import PredictableModel
from frec.recognizers.dataset import DataSet

class Recognizer(object):
    def __init__(self, size=(50, 50)):
        feature = ChainOperator(TanTriggsPreProcessing(), LBP())
        classifier = NearestNeighbor(dist_metric=ChiSquareDistance())

        self.predictor = PredictableModel(feature, classifier)

        self.dataSet = DataSet(size=size)
        self.compute()

    def compute(self):
        people = []
        photos = []

        for person in self.dataSet.data.keys():
            people.append(person)
            photos.append(self.dataSet.data[person])

        self.predictor.compute(photos, np.array(people, dtype=np.int))

    def recognize(self, image):
        return self.predictor.predict(image.grayscale().to_array())

    def train(self, person, images):
        self.dataSet.train(person, images)

