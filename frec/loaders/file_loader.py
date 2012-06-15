#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

# code adapted from thumbor's file loader module (http://github.com/globocom/thumbor)

from os.path import join, exists

def load(context, path, callback):
    file_path = join(context.config.FILE_LOADER_ROOT_PATH.rstrip('/'), path.lstrip('/'))

    if not exists(file_path):
        callback(None)
    else:
        with open(file_path, 'r') as f:
            callback(f.read())
