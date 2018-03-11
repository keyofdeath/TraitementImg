#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ImgOperator import *
import cv2

if __name__ == "__main__":

    # operator1 = ImgOprerator("../imgSample/pic_6.jpg")
    # operator1.add_oporation(ImgTranslation([[330, 60], [534, 156], [129, 317], [358, 464]]))

    # operator2 = ImgOprerator("out.jpg")
    # operator2.add_oporation(ImgTranslation([[232, 93], [383, 121], [346, 331], [197, 307]]))
    # cv2.imshow("res 1", operator2.img)

    operator3 = ImgOprerator("../imgSample/pic_3.jpg")
    operator3.add_oporation(ImgTranslation([[353, 56], [550, 132],
                                            [200, 308], [417, 421]]))

    cv2.imshow("res 2", operator2.img)
    cv2.waitKey(0)
