#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ImgOperator.Oporation import Oporation
from ImgOperator.Trasformations.VisionTool import *
from ImgOperator.Tool import *
import numpy as np
import cv2


class ImgTranslation(Oporation):

    def __init__(self, corner_position):
        """
        H = Haut
        B = Bas
        D = Droit
        G = Gauche
                                                        0                       1
        :param corner_position: Sous la forme [ [HG X, HG Y, ou HG Z], [HD X, HD Y, ou HD Z],
                                                                ..Autre point..
                                                        -2                      -1
                                                [BG X, BG Y, ou BG Z], [BD X, BD Y, ou BD Z] ]
        """
        super().__init__()
        self.corn_pos = corner_position
        self.out_height = max(abs(self.corn_pos[0][1] - self.corn_pos[-2][1]),
                              abs(self.corn_pos[1][1] - self.corn_pos[-1][1]))

        self.out_width = max(abs(self.corn_pos[0][0] - self.corn_pos[1][0]),
                             abs(self.corn_pos[-2][0] - self.corn_pos[-1][0]))

        self.out_position = [[0, 0], [self.out_width, 0], [0, self.out_height], [self.out_width, self.out_height]]
        self.mat_l = dlt(2, self.corn_pos, self.out_position)[0]

    def apply(self, img):
        # image de fin
        img_out = creat_empty_img(self.out_height, self.out_width)

        for y in range(self.out_height):
            for x in range(self.out_width):
                img_pos = dlt_reconstruction(2, 1, self.mat_l, [x, y])
                img_out[y][x] = img[int(img_pos[1])][int(img_pos[0])]
        cv2.imshow("res", img_out)
        cv2.waitKey(0)


if __name__ == "__main__":
    pass
