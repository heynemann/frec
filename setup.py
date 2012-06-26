#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

from setuptools import setup, Extension

import numpy as np

from frec import __version__

def extension(name, files):
    return Extension(name, files, include_dirs = [np.get_include()])

def run_setup():
    setup(
        name = 'frec',
        version = __version__,
        description = 'frec is a service that builds a database of recognizable faces upon time.',
        long_description = """
            frec is a service that builds a database of recognizable faces upon time.
        """,
        keywords = 'imaging face detection recognition feature lbp tantriggs opencv',
        author = 'Bernardo Heynemann',
        author_email = 'heynemann@gmail.com',
        url = 'https://heynemann.github.com/frec',
        license = 'MIT',
        classifiers = ['Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: MacOS',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 2.6',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Multimedia :: Graphics :: Presentation'
        ],
        packages = ['frec'],
        package_dir = {"frec": "frec"},
        include_package_data = True,
        package_data = {
        },

        install_requires=[
            "tornado>=2.1.1,<2.2.0",
        ],

        entry_points = {
            'console_scripts': [
                'frec = frec.server:main',
            ],
        },

        ext_modules = [
            extension(
                "frec.extensions._distance", 
                ["./frec/extensions/_distance.c"]
            )
        ]
    )

try:
    run_setup()
except SystemExit as exit:
    print "\n\n*******************************************************************"
    print "Couldn't build one or more native extensions, skipping compilation.\n\n"
    run_setup()
