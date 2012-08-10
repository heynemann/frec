#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join, exists

import scipy.io
from r3.worker.mapper import Mapper

from frec.recognizers import lbp
import frec.image as image

FEATURES_PATH = abspath(join(dirname(__file__), '..', 'vows', 'fixtures', 'features'))

FACES_PATH = abspath(join(dirname(__file__), '..', 'vows', 'orl_faces'))
image_path = lambda person, picture: join(
    FACES_PATH, 's%d' % person, '%d.pgm' % picture
)

image_path = lambda person, picture: join(
    FACES_PATH, 's%d' % person, '%d.pgm' % picture
)

feature_path = lambda person, picture: join(
    FEATURES_PATH, '%d_%d' % (person, picture)
)

class FaceRecMapper(Mapper):
    job_type = 'face-rec'

    def __init__(self, *args, **kw):
        Mapper.__init__(self, *args, **kw)
        self.recognizer = lbp.Recognizer()

        #print "Training recognizer..."
        #for person in range(1, 41):
            #pictures = []
            #for picture in range(1, 11):
                #file_path = image_path(person, picture)
                #img = image.Image.create_from_buffer(self.read(file_path))
                #pictures.append(img)
            #self.recognizer.train("Pessoa %d" % person, pictures)

        #print "Computing recognizer..."
        #self.recognizer.compute()
        #print "Recognizer ready!"

    def read(self, path):
        with open(path, 'rb') as f:
            contents = f.read()
            return contents

    def map(self, images):
        return list(self.recognize(images))

    def get_feature_for(self, person, picture):
        feature = feature_path(person, picture)
        if exists("%s.mat" % feature):
            contents = scipy.io.loadmat(feature)
            return contents['m']

        contents = self.read(image_path(person, picture))
        img = image.Image.create_from_buffer(contents)
        img.grayscale()

        feat_data = self.recognizer.predictor.feature.extract(img.to_array())

        scipy.io.savemat(feature, {'m': feat_data})
        return feat_data

    def recognize(self, image_paths):
        for image_data in image_paths:
            person_to_detect, picture_to_detect, person, picture = image_data

            img_feature = self.get_feature_for(person_to_detect, picture_to_detect)
            feature = self.get_feature_for(person, picture)

            yield (person, self.recognizer.predictor.classifier.dist_metric(feature, img_feature))

