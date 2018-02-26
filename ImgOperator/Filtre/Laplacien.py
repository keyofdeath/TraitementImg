#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ImgOperator.Filtre.Filtre import Filtre
import numpy as np


class Laplacien(Filtre):

    def __init__(self):
        super().__init__()
        self.convol = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]

    def apply(self, img):
        return np.convolve(img, self.convol)


if __name__ == "__main__":
    pass
