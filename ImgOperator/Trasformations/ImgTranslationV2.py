#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ImgOperator.Oporation import Oporation
from ImgOperator.Trasformations.VisionTool import *
from ImgOperator.Tool import *
import numpy as np
import cv2


class ImgTranslationV2(Oporation):

    def __init__(self, corner_position):
        """
        H = Haut
        B = Bas
        D = Droit
        G = Gauche
                                                    0           1
        :param corner_position: Sous la forme [ [HG Y, GG X], [HD Y, HD X],
                                                    2           3
                                                [BG Y, BG X], [BD Y, BD X] ]
        """
        super().__init__()
        self.corn_pos = corner_position

    def apply(self, img):

        # on recupaire tour nos point (x) sur le bord gauche de notre image
        list_point_l = get_all_pix_between_2_point(self.corn_pos[0], self.corn_pos[2], 0)
        # on recupaire tour nos point (x) sur le bord droit de notre image
        list_point_r = get_all_pix_between_2_point(self.corn_pos[1], self.corn_pos[3], 0)
        # pour l'instant comme on ne j'aire pas les bords plus petit que l'autre on parcour le bord le plus petit
        l = len(list_point_l) if len(list_point_l) <= len(list_point_r) else len(list_point_r)
        # creation d'une image vide
        height = max(abs(self.corn_pos[0][0] - self.corn_pos[2][0]), abs(self.corn_pos[1][0] - self.corn_pos[3][0]))
        width = max(abs(self.corn_pos[0][1] - self.corn_pos[1][1]), abs(self.corn_pos[2][1] - self.corn_pos[3][1]))
        # pnc hop le y le plus petit pour le décaler sur notre image recadrer
        min_y = sorted(self.corn_pos, key=lambda v: v[0])[0][0]
        min_x = sorted(self.corn_pos, key=lambda v: v[1])[0][1]
        print(min_y)
        img_out = creat_empty_img(600, 600)
        for i in range(l):
            #                                               n chop tout la ligne selon l'axe des X
            img_out[list_point_l[i][0]][list_point_l[i][1]:list_point_r[i][1]] = img[list_point_l[i][0]][list_point_l[i][1]:list_point_r[i][1]]
        cv2.imshow("main", img_out)
        cv2.waitKey(0)


if __name__ == "__main__":
    pass
