#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join

class FaceRecStream:
    job_type = 'face-rec'
    group_size = 30

    def process(self, app, arguments):
        person = int(arguments['person'][0])
        picture = int(arguments['picture'][0])
        return list(self.get_data(person, picture))

    def get_data(self, person_to_detect, picture_to_detect):
        for person in range(1, 41):
            for picture in range(1, 11):
                yield (person_to_detect, picture_to_detect, person, picture)

