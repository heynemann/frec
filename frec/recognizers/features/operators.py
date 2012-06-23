#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

# code adapted from facerec's feature module (https://github.com/bytefish/facerec)

from frec.recognizers.features import AbstractFeature

class FeatureOperator(AbstractFeature):
    """
    A FeatureOperator operates on two feature models.

    Args:
        first_feature [AbstractFeature]
        second_feature [AbstractFeature]
    """
    def __init__(self, first_feature, second_feature):
        if (not isinstance(first_feature, AbstractFeature)) or \
           (not isinstance(second_feature, AbstractFeature)):
            raise ValueError("A FeatureOperator only works on classes implementing an AbstractFeature!")
        self.first_feature = first_feature
        self.second_feature = second_feature

    def __repr__(self):
        return "FeatureOperator(" + repr(self.first_feature) + "," + repr(self.second_feature) + ")"

class ChainOperator(FeatureOperator):
    """
    The ChainOperator chains two feature extraction modules:
        second_feature.compute(first_feature.compute(X,y),y)
    Where X can be generic input data.

    Args:
        first_feature [AbstractFeature]
        second_feature [AbstractFeature]
    """
    def __init__(self, first_feature, second_feature):
        FeatureOperator.__init__(self, first_feature, second_feature)

    def compute(self, x, y):
        x = self.first_feature.compute(x, y)
        return self.second_feature.compute(x, y)

    def extract(self, x):
        x = self.first_feature.extract(x)
        return self.second_feature.extract(x)

    def __repr__(self):
        return "ChainOperator(" + repr(self.first_feature) + "," + repr(self.second_feature) + ")"

