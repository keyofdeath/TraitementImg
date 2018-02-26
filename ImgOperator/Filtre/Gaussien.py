#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ImgOperator.Filtre.Filtre import Filtre


class Gaussien(Filtre):

    def __init__(self, largeur=5, hauteur=5, seuil=1.4):
        super().__init__()

    def apply(self, img):
        pass


if __name__ == "__main__":
    pass