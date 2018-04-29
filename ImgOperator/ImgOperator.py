#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from ImgOperator.Oporation import Oporation


class ImgOprerator(object):

    def __init__(self, path_img_or_img):
        """

        :param path_img_or_img: Chemin vers une image ou une image charger par openCv
        """

        self.path_img = path_img_or_img if type(path_img_or_img) == str else None
        self.img = cv2.imread(self.path_img) if self.path_img is not None else path_img_or_img.copy()
        self.operation_list = list()

    def add_oporation(self, oporation):
        """
        Ajoute une opération a faire sur l'image
        :param oporation: opération a appliquer sur l'image
        :return:
        """

        if oporation.__class__.__bases__[-1] != Oporation:
            raise TypeError("Error: the type is not an Oporation type")
        self.img = oporation.apply(self.img)
        self.operation_list.append(oporation)

    def save_img(self, name):
        """
        Sauvgarde l'ime
        :param name:
        :return:
        """

        cv2.imwrite(name, self.img)


if __name__ == "__main__":
    pass
