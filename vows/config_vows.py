#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2012 Bernardo Heynemann heynemann@gmail.com

from os.path import abspath, dirname, join

from pyvows import Vows, expect

from frec.config import Config, ConfigurationError

TEST_DATA = (
    ('FILE_LOADER_ROOT_PATH', '/tmp/frec'),
    ('REDIS_STORAGE_SERVER_HOST', 'localhost'),
    ('REDIS_STORAGE_SERVER_PORT', 6379),
    ('REDIS_STORAGE_SERVER_DB', 0),
)


@Vows.batch
class Configuration(Vows.Context):

    class DefaultFrecConf(Vows.Context):
        def topic(self):
            for data in TEST_DATA:
                yield data

        class VerifyDefaultValueContext(Vows.Context):
            def topic(self, data):
                key, default_value = data
                cfg = Config()
                return (getattr(cfg, key), default_value)

            def should_have_default_value(self, topic):
                actual, expected = topic
                expect(actual).not_to_be_null()
                expect(actual).to_equal(expected)

        class VerifyLoadedValue(Vows.Context):
            def topic(self, data):
                key, default_value = data
                config_path = abspath(join(
                    dirname(__file__),
                    'config_vows_frec.conf'
                ))
                cfg = Config.load(config_path)
                return (getattr(cfg, key), default_value)

            def should_have_default_value(self, topic):
                actual, expected = topic
                expect(actual).not_to_be_null()
                expect(actual).to_equal(expected)

        class VerifyLoadedValueWithDefaultPath(Vows.Context):
            def topic(self, data):
                key, default_value = data
                cfg = Config.load()
                return (getattr(cfg, key), default_value)

            def should_have_default_value(self, topic):
                actual, expected = topic
                expect(actual).not_to_be_null()
                expect(actual).to_equal(expected)

    class GetConfFilePath(Vows.Context):

        def topic(self):
            return Config.get_conf_file()

        def should_have_default_value(self, topic):
            expected = abspath(join(dirname(__file__), '../frec/frec.conf'))
            expect(topic).to_equal(expected)

    class ConfigWithDefaults(Vows.Context):

        def topic(self):
            cfg = Config(defaults={
                'some_random_key': 'some_random_value'
            })

            cfg.validates_presence_of('some_random_key')
            return cfg

        def should_have_random_key(self, topic):
            expect(topic.get('some_random_key')).to_equal('some_random_value')
            expect(topic.some_random_key).to_equal('some_random_value')

        def should_validate_presence(self, topic):
            expect(topic).not_to_be_an_error()

    class ConfigValidatePresenceError(Vows.Context):

        def topic(self):
            cfg = Config()
            cfg.validates_presence_of('some_random_key')

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()
            expect(topic).to_be_an_error_like(ConfigurationError)

    class ConfigGetWithDefault(Vows.Context):

        def topic(self):
            cfg = Config()
            return cfg.get('some_random_key', 'override')

        def should_be_override(self, topic):
            expect(topic).to_equal('override')
