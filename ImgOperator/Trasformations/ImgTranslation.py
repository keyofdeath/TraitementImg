#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ImgOperator.Oporation import Oporation
from ImgOperator.Trasformations.VisionTool import *
from ImgOperator.Tool import *
import numpy as np
import cv2


def homogenisation(vect):
    """

    :param vect:
    :return:
    """
    return np.concatenate((np.asarray(vect), [1]))


def un_homogenisation(vect):
    """

    :param vect:
    :return:
    """
    return np.asarray(np.asarray(vect)[:-1])


class ImgTranslation(Oporation):

    def __init__(self, corner_position, out_position):
        """
        H = Haut
        B = Bas
        D = Droit
        G = Gauche
        :param corner_position: Sous la forme [ [HG X, HG Y, HG Z], [HD X, HD Y, HD Z],
                                                [BG X, BG Y, BG Z], [BD X, BD Y, BD Z] ]

        :param out_position: Position de sortie de la transformation
        Sous la forme [ [HG X, HG Y, HG Z], [HD X, HD Y, HD Z],
                        [BG X, BG Y, BG Z], [BD X, BD Y, BD Z] ]
        """
        super().__init__()
        self.corn_pos = corner_position
        self.out_pos = out_position

    def apply(self, img):

        trans = DLT(np.transpose(self.corn_pos), np.transpose(self.out_pos))
        print(trans)
        # imgrows, imgcols, ch = img.shape
        # corners = [[0, 0], [0, imgcols], [imgrows, 0], [imgrows, imgcols]]
        # newcorners = np.asarray(
        #     [np.dot(trans, homogenisation(corner)) / np.dot(trans, homogenisation(corner))[-1] for corner in corners]
        # )
        # newcorners = np.asarray([un_homogenisation(nc / nc[-1]) for nc in newcorners])
        #
        # imgtrans = np.zeros([np.uint(newcorners[:, 0].max() - newcorners[:, 0].min() + 1),
        #                      np.uint(newcorners[:, 1].max() - newcorners[:, 1].min() + 1),
        #                      ch], dtype=np.uint8)
        #
        # transinv = np.linalg.inv(trans)
        #
        # print('img rows, cols, ch', imgrows, imgcols, ch)
        # print('imgtrans rows, cols, ch', imgtrans.shape[0], imgtrans.shape[1], imgtrans.shape[2])
        #
        # for i in range(0, imgtrans.shape[0] - 1):
        #     for j in range(0, imgtrans.shape[1] - 1):
        #         pt = homogenisation([(i + int(newcorners[:, 0].min())), (j + int(newcorners[:, 1].min()))])
        #         [x, y, z] = np.dot(transinv, pt)
        #         [x, y] = [x / z, y / z]
        #
        #         if 0 <= x < imgrows and 0 <= y < imgcols:
        #             imgtrans[i, j, :] = img[int(x), int(y), :]
        # cv2.imshow("res", imgtrans)
        # cv2.waitKey(0)
        # return imgtrans


if __name__ == "__main__":
    pass
