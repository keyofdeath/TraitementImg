#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from ImgOperator.Oporation import Oporation


class ImgOprerator(object):

    def __init__(self, path_img):
        self.path_img = path_img
        self.img = cv2.imread(self.path_img)
        self.operation_list = list()

    def add_oporation(self, oporation):

        if oporation.__class__.__bases__[-1] != Oporation:
            raise TypeError("Error: the type is not an Oporation type")
        oporation.apply(self.img)
        self.operation_list.append(oporation)


if __name__ == "__main__":
    pass
