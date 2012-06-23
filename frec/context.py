#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2012 Bernardo Heynemann heynemann@gmail.com

# code adapted from thumbor's context module
# (http://github.com/globocom/thumbor)


class Context:
    '''
    Class responsible for containing:
    * Server Configuration Parameters (port, ip, etc);
    * Configurations read from config file (or defaults);
    * Importer with imported modules (engine, filters, detectors, etc);
    '''

    def __init__(self, server=None, config=None, importer=None):
        self.server = server
        self.config = config

        if importer:
            self.modules = ContextImporter(self, importer)
        else:
            self.modules = None


class ServerParameters:
    def __init__(self, port, ip, config_path, log_level, app_class):
        self.port = port
        self.ip = ip
        self.config_path = config_path
        self.log_level = log_level
        self.app_class = app_class


class ContextImporter:
    def __init__(self, context, importer):
        self.context = context
        self.importer = importer

        #self.engine = None
        #if importer.engine:
            #self.engine = importer.engine(context)
