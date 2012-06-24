#!/usr/bin/python
# -*- coding: utf-8 -*-

# frec face recognition service
# https://github.com/heynemann/frec

# licensed under the mit license:
# http://www.opensource.org/licenses/mit-license
# copyright (c) 2012 bernardo heynemann heynemann@gmail.com

# code adapted from facerec's feature module
# (https://github.com/bytefish/facerec)

import numpy as np

from frec.recognizers.features import AbstractFeature


class FeatureOperator(AbstractFeature):
    """
    A FeatureOperator operates on two feature models.

    Args:
        first_feature [AbstractFeature]
        second_feature [AbstractFeature]
    """
    def __init__(self, first_feature, second_feature):
        if (not isinstance(first_feature, AbstractFeature)) or \
           (not isinstance(second_feature, AbstractFeature)):
            raise ValueError("A FeatureOperator only works on classes implementing an AbstractFeature!")
        self.first_feature = first_feature
        self.second_feature = second_feature

    def __repr__(self):
        return "FeatureOperator(" + repr(self.first_feature) + "," + repr(self.second_feature) + ")"


class ChainOperator(FeatureOperator):
    """
    The ChainOperator chains two feature extraction modules:
        second_feature.compute(first_feature.compute(X,y),y)
    Where X can be generic input data.

    Args:
        first_feature [AbstractFeature]
        second_feature [AbstractFeature]
    """
    def __init__(self, first_feature, second_feature):
        FeatureOperator.__init__(self, first_feature, second_feature)

    def compute(self, x, y):
        x = self.first_feature.compute(x, y)
        return self.second_feature.compute(x, y)

    def extract(self, x):
        x = self.first_feature.extract(x)
        return self.second_feature.extract(x)

    def __repr__(self):
        return "ChainOperator(" + repr(self.first_feature) + "," + repr(self.second_feature) + ")"


class LBPOperator(object):
    def __init__(self, neighbors):
        self._neighbors = neighbors

    def __call__(self, x):
        raise NotImplementedError(
            "Every LBPOperator must implement the __call__ method.")

    @property
    def neighbors(self):
        return self._neighbors

    def __repr__(self):
        return "LBPOperator (neighbors=%s)" % self.neighbors


class ExtendedLBP(LBPOperator):
    def __init__(self, radius=1, neighbors=8):
        LBPOperator.__init__(self, neighbors=neighbors)
        self._radius = radius

    def __call__(self, x):
        x = np.asanyarray(x)
        y_size, x_size = x.shape[0], x.shape[1]

        # define circle
        angles = 2 * np.pi / self._neighbors
        theta = np.arange(0, 2 * np.pi, angles)

        # calculate sample points on circle with radius
        sample_points = np.array([-np.sin(theta), np.cos(theta)]).T
        sample_points *= self._radius

        # find boundaries of the sample points
        min_y = min(sample_points[:, 0])
        max_y = max(sample_points[:, 0])
        min_x = min(sample_points[:, 1])
        max_x = max(sample_points[:, 1])

        # calculate block size, each LBP code is computed within a block of
        # size bsizey*bsizex
        block_size_y = np.ceil(max(max_y, 0)) - np.floor(min(min_y, 0)) + 1
        block_size_x = np.ceil(max(max_x, 0)) - np.floor(min(min_x, 0)) + 1

        # coordinates of origin (0,0) in the block
        orig_y = 0 - np.floor(min(min_y, 0))
        orig_x = 0 - np.floor(min(min_x, 0))

        # calculate output image size
        dx = x_size - block_size_x + 1
        dy = y_size - block_size_y + 1

        # get center points
        center_points = np.asarray(
            x[orig_y:orig_y + dy, orig_x:orig_x + dx],
            dtype=np.uint8
        )
        result = np.zeros((dy, dx), dtype=np.uint32)

        for i, p in enumerate(sample_points):
            # get coordinate in the block
            sample_y, sample_x = p + (orig_y, orig_x)

            # Calculate floors, ceils and rounds for the x and y.
            fx = np.floor(sample_x)
            fy = np.floor(sample_y)
            cx = np.ceil(sample_x)
            cy = np.ceil(sample_y)

            # calculate fractional part
            ty = sample_y - fy
            tx = sample_x - fx

            # calculate interpolation weights
            w1 = (1 - tx) * (1 - ty)
            w2 = tx * (1 - ty)
            w3 = (1 - tx) * ty
            w4 = tx * ty

            # calculate interpolated image
            n = w1 * x[fy:fy + dy, fx:fx + dx]
            n += w2 * x[fy:fy + dy, cx:cx + dx]
            n += w3 * x[cy:cy + dy, fx:fx + dx]
            n += w4 * x[cy:cy + dy, cx:cx + dx]

            # update LBP codes
            delta = n >= center_points
            result += (1 << i) * delta
        return result

    @property
    def radius(self):
        return self._radius

    def __repr__(self):
        return "ExtendedLBP (neighbors=%s, radius=%s)" % (self._neighbors, self._radius)


class LBP(AbstractFeature):
    def __init__(self, lbp_operator=None, size=(8, 8)):
        AbstractFeature.__init__(self)

        if lbp_operator is None:
            lbp_operator = ExtendedLBP()

        if not isinstance(lbp_operator, LBPOperator):
            raise TypeError("Only an operator of type facerec.lbp.LBPOperator is a valid lbp_operator.")

        self.lbp_operator = lbp_operator
        self.size = size

    def compute(self, x, y):
        features = []

        for value in x:
            features.append(self.extract(value))

        return features

    def extract(self, x):
        x = np.asarray(x)
        return self.spatially_enhanced_histogram(x)

    def spatially_enhanced_histogram(self, x):
        # calculate the LBP image
        lbp_image = self.lbp_operator(x)

        # calculate the grid geometry
        lbp_height, lbp_width = lbp_image.shape
        grid_rows, grid_cols = self.size
        py = int(np.floor(lbp_height / grid_rows))
        px = int(np.floor(lbp_width / grid_cols))

        enhanced_histogram = []
        for row in range(0, grid_rows):
            for col in range(0, grid_cols):
                y_low = row * py
                y_hi = (row + 1) * py
                x_low = col * px
                x_hi = (col + 1) * px

                center_points = lbp_image[y_low:y_hi, x_low:x_hi]

                histogram = np.histogram(
                    center_points,
                    bins=2 ** self.lbp_operator.neighbors,
                    range=(0, 2 ** self.lbp_operator.neighbors),
                    normed=True
                )[0]

                # probably useful to apply a mapping?
                enhanced_histogram.extend(histogram)

        return np.asarray(enhanced_histogram)

    def __repr__(self):
        return "Local Binary Pattern (operator=%s, grid=%s)" % (repr(self.lbp_operator), str(self.size))
