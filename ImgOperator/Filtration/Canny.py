#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ImgOperator.Oporation import Oporation
import cv2
import numpy as np


class ImgCanny(Oporation):

    def __init__(self, sigma=0.33):
        super().__init__()
        self.sigma = sigma

    def apply(self, img):

        # compute the median of the single channel pixel intensities
        v = np.median(img)

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - self.sigma) * v))
        upper = int(min(255, (1.0 + self.sigma) * v))
        edged = cv2.Canny(img, lower, upper)

        # return the edged image
        return edged


if __name__ == "__main__":
    pass