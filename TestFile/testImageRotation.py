#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ImgOperator import *


if __name__ == "__main__":

    operator1 = ImgOprerator("../imgSample/pic_6.jpg")
    operator1.add_oporation(ImgTranslation([[330, 60], [534, 156], [129, 317], [358, 464]]))

    # operator2 = ImgOprerator("../imgSample/pic_2.jpg")
    # operator2.add_oporation(ImgTranslation([[89, 230], [92, 456], [426, 207], [431, 469]]))

    operator3 = ImgOprerator("../imgSample/pic_3.jpg")
    operator3.add_oporation(ImgTranslation([[353, 56], [550, 132],
                                            [200, 308], [417, 421]]))
