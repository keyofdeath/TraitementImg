#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ImgOperator.Oporation import Oporation
from ImgOperator.Tool import creat_empty_img
import numpy as np
import cv2


class ImgTranslation(Oporation):

    def __init__(self, corner_position):
        """
        H = Haut
        B = Bas
        D = Droit
        G = Gauche
        :param corner_position: Sous la forme [ [Y start, Y end],[x start, x end]
        """
        super().__init__()
        self.corner_position = corner_position

    def apply(self, img):

        print(self.corner_position)
        print(img[np.ix_(self.corner_position[0], self.corner_position[1])])
        img_out = img[self.corner_position[0][0]:self.corner_position[0][1], self.corner_position[1][0]:self.corner_position[1][1]].copy()
        cv2.imshow("main", img_out)
        cv2.waitKey(0)


if __name__ == "__main__":
    pass
