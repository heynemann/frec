#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

# code adapted from thumbor's config module (http://github.com/globocom/thumbor)

import os
from os.path import join, exists, expanduser, dirname, abspath
import imp

class ConfigurationError(RuntimeError):
    pass

class Config(object):
    class_defaults = {}

    @classmethod
    def define(cls, key, value):
        cls.class_defaults[key] = value

    @classmethod
    def get_conf_file(cls):
        lookup_conf_file_paths = [
            os.curdir,
            expanduser('~'),
            '/etc/',
            dirname(__file__)
        ]

        for conf_path in lookup_conf_file_paths:
            conf_path_file = abspath(join(conf_path, 'frec.conf'))
            if exists(conf_path_file):
                return conf_path_file

        raise ConfigurationError('frec.conf file not passed and not found on the lookup paths %s' % lookup_conf_file_paths)

    @classmethod
    def load(cls, path=None):
        if path is None:
            path = cls.get_conf_file()

        with open(path) as config_file:
            name='configuration'
            code = config_file.read()
            module = imp.new_module(name)
            exec code in module.__dict__

            conf = cls()
            conf.config_file = path
            for name, value in module.__dict__.iteritems():
                setattr(conf, name, value)

            return conf

    def __init__(self, **kw):
        if 'defaults' in kw:
            self.defaults = kw['defaults']

        for key, value in kw.iteritems():
            setattr(self, key, value)

    def validates_presence_of(self, *args):
        for arg in args:
            if not hasattr(self, arg):
                raise ConfigurationError('Configuration %s was not found and does not have a default value. Please verify your frec.conf file' % arg)

    def get(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        return default

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        if 'defaults' in self.__dict__ and name in self.__dict__['defaults']:
            return self.__dict__['defaults'][name]

        if name in Config.class_defaults:
            return Config.class_defaults[name]

        raise AttributeError(name)

# FILE LOADER OPTIONS
Config.define('FILE_LOADER_ROOT_PATH', '/tmp/frec')

# REDIS STORAGE OPTIONS
Config.define('REDIS_STORAGE_SERVER_HOST', 'localhost')
Config.define('REDIS_STORAGE_SERVER_PORT', 6379)
Config.define('REDIS_STORAGE_SERVER_DB', 0)
Config.define('REDIS_STORAGE_SERVER_PASSWORD', None)

