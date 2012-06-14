#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

# code adapted from thumbor's util module (http://github.com/globocom/thumbor)

import logging

def real_import(name):
    if '.'  in name:
        return reduce(getattr, name.split('.')[1:], __import__(name))
    return __import__(name)

logger = logging.getLogger('frec')
