#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from pyvows import Vows, expect

from frec.importer import Importer
from frec.config import Config
import frec.loaders.file_loader as file_loader

test_data = [
    ('loader', file_loader),
]

@Vows.batch
class ImporterVows(Vows.Context):

    class AllConfigurationVows(Vows.Context):
        def topic(self):
            for data in test_data:
                complete_config = Config(
                    loader='frec.loaders.file_loader'
                )

                yield data, complete_config

        class CanImportItem(Vows.Context):
            def topic(self, test_item):
                test_data, config = test_item
                importer = Importer(config)
                importer.import_modules()

                if hasattr(importer, test_data[0].lower()):
                    return (getattr(importer, test_data[0].lower()), test_data[1])
                return (None, None)

            def should_be_proper_item(self, topic):
                if topic[0] is tuple:
                    for index, item in enumerate(topic[0]):
                        expect(item).not_to_be_null()
                        expect(item).to_equal(topic[1][index])
                else:
                    expect(topic[0]).not_to_be_null()
                    expect(topic[0]).to_equal(topic[1])

    #class ImportWithFixedValueVows(Vows.Context):

        #class SingleItem(Vows.Context):
            #def topic(self):
                #importer = Importer(None)
                #importer.import_item(config_key='file_storage', item_value='thumbor.storages.file_storage', class_name='Storage')
                #return importer.file_storage

            #def should_equal_file_storage(self, topic):
                #expect(topic).to_equal(file_storage)

        #class MultipleItems(Vows.Context):
            #def topic(self):
                #importer = Importer(None)
                #importer.import_item(config_key='detectors', item_value=('thumbor.detectors.feature_detector', 'thumbor.detectors.feature_detector'), is_multiple=True)
                #return importer.detectors

            #def should_have_length_of_2(self, topic):
                #expect(topic).to_length(2)

            #def should_contain_both_detectors(self, topic):
                #expect(topic).to_include(feature_detector)
