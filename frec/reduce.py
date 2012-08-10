#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

class FaceRecReducer:
    job_type = 'face-rec'

    def reduce(self, app, items):
        min_distance = sys.maxint
        min_person = None

        for people in items:
            for person in people:
                if person[1] < min_distance:
                    min_distance = person[1]
                    min_person = person[0]

        return {
            'person': min_person,
            'distance': min_distance
        }
