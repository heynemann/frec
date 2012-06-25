#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

from pyvows import Vows, expect

import frec.recognizers.dataset as ds


@Vows.batch
class DataSet(Vows.Context):
    def topic(self):
        return ds.DataSet()

    def should_be_instance_of(self, topic):
        expect(topic).to_be_instance_of(ds.DataSet)

    def should_have_empty_data(self, topic):
        expect(topic.data).to_be_empty()
