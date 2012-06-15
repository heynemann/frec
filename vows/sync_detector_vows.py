#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect

import frec.detectors.sync_detector as detector

@Vows.batch
class SyncDetector(Vows.Context):
    class ShouldReturnDetectedItemsInPicture(Vows.Context):
        def topic(self):

            return loader.load(context, 'some/invalid/path', callback)

        def should_be_none(self, topic):
            expect(topic.args[0]).to_be_null()

    class ShouldReturnContentIfProper(Vows.Context):
        @Vows.async_topic
        def topic(self, callback):
            context = ctx.Context(config=cfg.Config())
            return loader.load(context, 'test.txt', callback)

        def should_be_none(self, topic):
            expect(topic.args[0]).to_equal('test_data')


