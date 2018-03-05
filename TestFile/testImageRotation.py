#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ImgOperator import *


if __name__ == "__main__":
    operator1 = ImgOprerator("../imgSample/pic_1.jpg")
    operator1.add_oporation(ImgTranslationV2([[89, 230], [92, 456], [426, 207], [431, 469]]))

    # operator2 = ImgOprerator("../imgSample/pic_2.jpg")
    # operator2.add_oporation(ImgTranslation([[89, 230], [92, 456], [426, 207], [431, 469]]))

    operator3 = ImgOprerator("../imgSample/pic_3.jpg")
    operator3.add_oporation(ImgTranslationV2([[56, 353], [132, 550], [308, 200], [421, 417]]))
    operator3.add_oporation(ImgTranslation([[353, 56, 1], [550, 132, 1], [200, 308, 1], [417, 421, 1]],
                                           [[0, 0, 1], [200, 0, 1], [0, 250, 1], [200, 250, 1]]))
    # operator.add_oporation(ImgTranslation([[89, 431], [230, 469]]))
