#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2012 Bernardo Heynemann heynemann@gmail.com

import os
import shutil

from pyvows import Vows, expect

import frec.loaders.file_loader as loader
import frec.context as ctx
import frec.config as cfg

if os.path.exists('/tmp/frec'):
    shutil.rmtree('/tmp/frec')
os.makedirs('/tmp/frec')

with open('/tmp/frec/test.txt', 'a') as f:
    f.write('test_data')

@Vows.batch
class FileLoaderVows(Vows.Context):
    class ShouldReturnNoneOnError(Vows.Context):
        @Vows.async_topic
        def topic(self, callback):
            context = ctx.Context(config=cfg.Config())
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


