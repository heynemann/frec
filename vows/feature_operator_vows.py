#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

from pyvows import Vows, expect

import frec.recognizers.features as features
import frec.recognizers.features.operators as operators

@Vows.batch
class FeatureOperator(Vows.Context):
    class WithProperFeatures(Vows.Context):
        def topic(self):
            return operators.FeatureOperator(features.AbstractFeature(), features.AbstractFeature())

        def should_be_instance_of(self, topic):
            expect(topic).to_be_instance_of(operators.FeatureOperator)

        def should_have_both_models(self, topic):
            expect(topic.model1).to_be_instance_of(features.AbstractFeature)
            expect(topic.model2).to_be_instance_of(features.AbstractFeature)

        class StringRepresentation(Vows.Context):
            def topic(self, feature):
                return str(feature)

            def should_be_abstract_feature(self, topic):
                expect(topic).to_equal('FeatureOperator(AbstractFeature,AbstractFeature)')


    class WithInvalidFeatures(Vows.Context):
        def topic(self):
            return operators.FeatureOperator("invalid", "features")

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()
            expect(topic).to_be_an_error_like(ValueError)
