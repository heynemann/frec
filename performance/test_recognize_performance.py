#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

import os.path as path
import os

import chrono as ch
import frec.recognizers.lbp as lbp
from frec.image import Image

ROOT_PATH = path.abspath(os.environ.get('ROOT_PATH', path.dirname(__file__)))
image_path = lambda person: path.join(
    ROOT_PATH, '%d.pgm' % person
)

cache = {}
def _read(path):
    if path in cache:
        return cache[path]
    with open(path, 'rb') as f:
        contents = f.read()
        cache[path] = contents
        return contents

PATH1 = image_path(1)
PATH2 = image_path(2)
IMG1 = Image.create_from_buffer(_read(PATH1))
IMG2 = Image.create_from_buffer(_read(PATH2))

def main(people_to_train, images_to_train, iterations):
    recognizer = lbp.Recognizer()

    train_timer = ch.Chrono('training')
    compute_timer = ch.Chrono('compute')
    recognize_timer = ch.Chrono('recognize')

    train_timer.start()
    for i in range(people_to_train):
        images = [IMG1 for i in range(images_to_train / 2)]
        images += [IMG2 for i in range(images_to_train / 2)]
        recognizer.train(i, images)
        train_timer.iterate()

    train_timer.stop()

    compute_timer.start()
    recognizer.compute()
    compute_timer.iterate()
    compute_timer.stop()

    recognize_timer.start()
    for i in range(iterations):
        recognizer.recognize(IMG2)
        recognize_timer.iterate()
    recognize_timer.stop()

    print train_timer
    print compute_timer
    print recognize_timer


if __name__ == '__main__':
    main(15, 100, 1)
